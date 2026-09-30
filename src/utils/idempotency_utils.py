"""Utilidades para garantizar idempotencia en operaciones de carga de datos.

Este módulo proporciona mecanismos para evitar duplicados y asegurar que las operaciones
de escritura sean idempotentes mediante estrategias de reintento y claves únicas.
"""

import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar
from dataclasses import dataclass, field
import pandas as pd

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class IdempotencyRecord:
    """Registro de una operación idempotente en el sistema."""
    key: str
    status: str  # 'pending', 'completed', 'failed'
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    retry_count: int = 0

    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Marca el registro como completado exitosamente."""
        self.status = 'completed'
        self.result = result
        self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error: str) -> None:
        """Marca el registro como fallido."""
        self.status = 'failed'
        self.error = error
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el registro a diccionario para serialización."""
        return {
            'key': self.key,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'retry_count': self.retry_count
        }


class IdempotencyStore:
    """Almacén de registros de idempotencia con soporte para múltiples backends."""

    def __init__(self, backend: str = 'memory', **kwargs):
        """Inicializa el almacén de idempotencia.

        Args:
            backend: Tipo de backend ('memory', 's3', 'dynamodb')
            **kwargs: Configuración específica del backend
        """
        self.backend = backend
        self._store: Dict[str, IdempotencyRecord] = {}
        self._s3_bucket = kwargs.get('s3_bucket')
        self._dynamodb_table = kwargs.get('dynamodb_table')

        if backend == 's3' and not self._s3_bucket:
            raise ValueError("S3 bucket requerido para backend 's3'")
        if backend == 'dynamodb' and not self._dynamodb_table:
            raise ValueError("DynamoDB table requerido para backend 'dynamodb'")

        logger.info(f"IdempotencyStore inicializado con backend: {backend}")

    def get(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera un registro de idempotencia por su clave."""
        if self.backend == 'memory':
            return self._store.get(key)
        elif self.backend == 's3':
            return self._get_from_s3(key)
        elif self.backend == 'dynamodb':
            return self._get_from_dynamodb(key)
        return None

    def save(self, record: IdempotencyRecord) -> None:
        """Guarda un registro de idempotencia."""
        if self.backend == 'memory':
            self._store[record.key] = record
        elif self.backend == 's3':
            self._save_to_s3(record)
        elif self.backend == 'dynamodb':
            self._save_to_dynamodb(record)

    def _get_from_s3(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera registro desde S3."""
        try:
            import boto3
            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=self._s3_bucket, Key=f"idempotency/{key}.json")
            data = json.loads(response['Body'].read().decode('utf-8'))
            return self._dict_to_record(data)
        except Exception as e:
            logger.debug(f"No se encontró registro en S3: {key} - {e}")
            return None

    def _save_to_s3(self, record: IdempotencyRecord) -> None:
        """Guarda registro en S3."""
        import boto3
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=self._s3_bucket,
            Key=f"idempotency/{record.key}.json",
            Body=json.dumps(record.to_dict()).encode('utf-8')
        )

    def _get_from_dynamodb(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera registro desde DynamoDB."""
        try:
            import boto3
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(self._dynamodb_table)
            response = table.get_item(Key={'idempotency_key': key})
            if 'Item' in response:
                return self._dict_to_record(response['Item'])
            return None
        except Exception as e:
            logger.debug(f"No se encontró registro en DynamoDB: {key} - {e}")
            return None

    def _save_to_dynamodb(self, record: IdempotencyRecord) -> None:
        """Guarda registro en DynamoDB."""
        import boto3
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self._dynamodb_table)
        table.put_item(Item=record.to_dict())

    @staticmethod
    def _dict_to_record(data: Dict[str, Any]) -> IdempotencyRecord:
        """Convierte diccionario a IdempotencyRecord."""
        record = IdempotencyRecord(
            key=data['key'],
            status=data['status'],
            result=data.get('result'),
            error=data.get('error'),
            retry_count=data.get('retry_count', 0)
        )
        if 'created_at' in data:
            record.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            record.completed_at = datetime.fromisoformat(data['completed_at'])
        return record


def generate_idempotency_key(*args, **kwargs) -> str:
    """Genera una clave de idempotencia única basada en los argumentos.

    Args:
        *args: Argumentos posicionales de la operación
        **kwargs: Argumentos nominales de la operación

    Returns:
        Clave de idempotencia única como string hexadecimal
    """
    canonical_repr = json.dumps(
        {'args': args, 'kwargs': kwargs},
        sort_keys=True,
        default=str
    )
    return hashlib.sha256(canonical_repr.encode('utf-8')).hexdigest()


def generate_batch_idempotency_key(
    source: str,
    batch_date: datetime,
    batch_sequence: int,
    content_hash: str
) -> str:
    """Genera clave de idempotencia para operaciones de carga por lotes.

    Args:
        source: Identificador de la fuente de datos
        batch_date: Fecha del lote
        batch_sequence: Número de secuencia del lote
        content_hash: Hash del contenido del lote

    Returns:
        Clave de idempotencia formateada
    """
    key_data = f"{source}:{batch_date.isoformat()}:{batch_sequence}:{content_hash}"
    return f"batch_{hashlib.sha256(key_data.encode('utf-8')).hexdigest()[:32]}"


class RetryStrategy:
    """Estrategia de reintento con backoff exponencial."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        """Configura la estrategia de reintento.

        Args:
            max_retries: Número máximo de reintentos
            base_delay: Delay base en segundos
            max_delay: Delay máximo en segundos
            exponential_base: Base del exponente para backoff
            jitter: Añadir aleatoriedad al delay
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Calcula el delay para un intento específico."""
        import random
        delay = min(self.base_delay * (self.exponential_base ** attempt), self.max_delay)
        if self.jitter:
            delay *= (0.5 + random.random())
        return delay


def idempotent_operation(
    store: IdempotencyStore,
    retry_strategy: Optional[RetryStrategy] = None,
    operation_name: str = "operation"
):
    """Decorador para hacer una función idempotente.

    Args:
        store: Almacén de idempotencia
        retry_strategy: Estrategia de reintento
        operation_name: Nombre de la operación para logs
    """
    if retry_strategy is None:
        retry_strategy = RetryStrategy()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            idempotency_key = generate_idempotency_key(operation_name, *args, **kwargs)

            existing = store.get(idempotency_key)
            if existing and existing.status == 'completed':
                logger.info(f"Operación idempotente completada previamente: {idempotency_key}")
                return existing.result

            if existing and existing.status == 'pending':
                logger.warning(f"Operación ya en progreso: {idempotency_key}")
                raise IdempotencyConflictError(
                    f"Operación {idempotency_key} ya está en progreso"
                )

            record = IdempotencyRecord(key=idempotency_key, status='pending')
            store.save(record)

            last_error = None
            for attempt in range(retry_strategy.max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    record.mark_completed(result if isinstance(result, dict) else {'result': result})
                    store.save(record)
                    logger.info(f"Operación idempotente completada: {idempotency_key}")
                    return result
                except Exception as e:
                    last_error = e
                    record.retry_count = attempt + 1

                    if attempt < retry_strategy.max_retries:
                        delay = retry_strategy.get_delay(attempt)
                        logger.warning(
                            f"Reintento {attempt + 1}/{retry_strategy.max_retries} "
                            f"para {idempotency_key} tras {delay:.2f}s: {str(e)}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"Operación idempotente fallida después de {attempt + 1} intentos: {idempotency_key}")

            record.mark_failed(str(last_error))
            store.save(record)
            raise last_error

        return wrapper
    return decorator


class IdempotencyConflictError(Exception):
    """Excepción lanzada cuando se detecta un conflicto de idempotencia."""
    pass


def check_duplicate_records(
    df: pd.DataFrame,
    unique_columns: list,
    source_identifier: str
) -> pd.DataFrame:
    """Identifica registros duplicados en un DataFrame.

    Args:
        df: DataFrame con los datos a verificar
        unique_columns: Columnas que definen unicidad
        source_identifier: Identificador de la fuente para logging

    Returns:
        DataFrame con los registros duplicados
    """
    if df.empty:
        return df

    duplicates = df[df.duplicated(subset=unique_columns, keep=False)]

    if not duplicates.empty:
        logger.warning(
            f"Se detectaron {len(duplicates)} registros duplicados "
            f"en fuente {source_identifier} por columnas: {unique_columns}"
        )

    return duplicates


def merge_idempotent(
    existing_df: pd.DataFrame,
    new_df: pd.DataFrame,
    key_columns: list,
    conflict_resolution: str = 'prefer_new'
) -> pd.DataFrame:
    """Fusiona dos DataFrames de manera idempotente.

    Args:
        existing_df: DataFrame con datos existentes
        new_df: DataFrame con nuevos datos
        key_columns: Columnas que definen la clave de fusión
        conflict_resolution: Estrategia de resolución de conflictos
                           ('prefer_new', 'prefer_old', 'max_timestamp')

    Returns:
        DataFrame fusionado de manera idempotente
    """
    if existing_df.empty:
        return new_df.copy()

    if new_df.empty:
        return existing_df.copy()

    combined = pd.concat([existing_df, new_df], ignore_index=True)
    merged = combined.drop_duplicates(subset=key_columns, keep='last')

    logger.info(
        f"Fusión idempotente: {len(existing_df)} existentes + {len(new_df)} nuevos "
        f"= {len(merged)} únicos"
    )

    return merged


class BatchIdempotencyManager:
    """Gestor de idempotencia especializado para cargas por lotes."""

    def __init__(self, store: IdempotencyStore):
        self.store = store

    def register_batch(
        self,
        source: str,
        batch_date: datetime,
        batch_sequence: int,
        record_count: int,
        content_hash: str
    ) -> str:
        """Registra un nuevo lote para procesamiento idempotente."""
        idempotency_key = generate_batch_idempotency_key(
            source, batch_date, batch_sequence, content_hash
        )

        existing = self.store.get(idempotency_key)
        if existing and existing.status == 'completed':
            logger.info(f"Lote ya procesado: {idempotency_key} ({record_count} registros)")
            return idempotency_key

        record = IdempotencyRecord(
            key=idempotency_key,
            status='pending',
            result={'source': source, 'batch_date': batch_date.isoformat(),
                    'record_count': record_count}
        )
        self.store.save(record)

        logger.info(f"Lote registrado: {idempotency_key} ({record_count} registros)")
        return idempotency_key

    def complete_batch(self, key: str, result: Dict[str, Any]) -> None:
        """Marca un lote como completado."""
        record = self.store.get(key)
        if record:
            record.mark_completed(result)
            self.store.save(record)
            logger.info(f"Lote completado: {key}")

    def fail_batch(self, key: str, error: str) -> None:
        """Marca un lote como fallido."""
        record = self.store.get(key)
        if record:
            record.mark_failed(error)
            self.store.save(record)
            logger.error(f"Lote fallido: {key} - {error}")