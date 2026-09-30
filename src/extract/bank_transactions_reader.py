"""
Lector de transacciones bancarias para el pipeline de análisis financiero.
Se conecta a la fuente de datos bancarios y extrae transacciones en bruto.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional
from dataclasses import dataclass, field

import pandas as pd
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class TransactionRecord:
    """Representa una transacción bancaria individual."""
    transaction_id: str
    account_id: str
    timestamp: datetime
    amount: float
    currency: str
    transaction_type: str
    description: str
    merchant_id: Optional[str] = None
    merchant_category: Optional[str] = None
    status: str = "completed"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "timestamp": self.timestamp.isoformat(),
            "amount": self.amount,
            "currency": self.currency,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "merchant_id": self.merchant_id,
            "merchant_category": self.merchant_category,
            "status": self.status,
            "metadata": self.metadata
        }


class BankTransactionsReader:
    """
    Clase principal para leer transacciones bancarias de múltiples fuentes.
    Soporta conexión a APIs de bancos, bases de datos y archivos en S3.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 1000)
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 5)
        self._s3_client = None
        self._db_connection = None
        self._api_session = None

    def _get_s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.source_credentials.get("aws_access_key"),
                aws_secret_access_key=self.source_credentials.get("aws_secret_key"),
                region_name=self.source_credentials.get("region", "us-east-1")
            )
        return self._s3_client

    def _get_db_connection(self):
        if self._db_connection is None:
            import psycopg2
            self._db_connection = psycopg2.connect(
                host=self.source_credentials.get("db_host"),
                port=self.source_credentials.get("db_port", 5432),
                database=self.source_credentials.get("db_name"),
                user=self.source_credentials.get("db_user"),
                password=self.source_credentials.get("db_password")
            )
        return self._db_connection

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (ClientError, BotoCoreError, Exception) as e:
                last_exception = e
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def read_from_api(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde API bancaria con paginación.
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        api_url = self.source_credentials.get("api_url")
        api_key = self.source_credentials.get("api_key")

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Request-ID": f"bankReader-{datetime.now().timestamp()}"
        }

        page = 1
        has_more = True

        while has_more:
            params = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "page": page,
                "page_size": self.batch_size
            }
            if account_ids:
                params["account_ids"] = ",".join(account_ids)

            try:
                response = session.get(
                    f"{api_url}/transactions",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                for txn_data in data.get("transactions", []):
                    yield self._parse_transaction(txn_data)

                has_more = data.get("has_more", False)
                page += 1

            except requests.RequestException as e:
                logger.error(f"API request failed: {str(e)}")
                raise

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde archivos en S3 con partición por fecha.
        """
        s3_client = self._get_s3_client()

        date_format = "%Y-%m-%d"
        date_range = pd.date_range(start_date, end_date, freq='D')

        for date_obj in date_range:
            date_str = date_obj.strftime(date_format)
            object_key = f"{prefix}/date={date_str}/transactions.parquet"

            try:
                response = s3_client.get_object(Bucket=bucket, Key=object_key)
                data = response['Body'].read()

                df = pd.read_parquet(pd.io.common.BytesIO(data))

                for _, row in df.iterrows():
                    yield self._row_to_transaction_record(row)

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == 'NoSuchKey':
                    logger.info(f"No transactions file for date {date_str}")
                    continue
                logger.error(f"S3 error reading {object_key}: {str(e)}")
                raise

    def read_from_database(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde base de datos PostgreSQL.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                transaction_id, account_id, timestamp, amount,
                currency, transaction_type, description,
                merchant_id, merchant_category, status, metadata
            FROM bank_transactions
            WHERE timestamp >= %s AND timestamp < %s
        """
        params = [start_date, end_date]

        if account_ids:
            query += " AND account_id = ANY(%s)"
            params.append(account_ids)

        query += " ORDER BY timestamp LIMIT %s OFFSET %s"

        offset = 0
        while True:
            cursor.execute(query, params + [self.batch_size, offset])
            rows = cursor.fetchall()

            if not rows:
                break

            for row in rows:
                yield TransactionRecord(
                    transaction_id=row[0],
                    account_id=row[1],
                    timestamp=row[2],
                    amount=float(row[3]),
                    currency=row[4],
                    transaction_type=row[5],
                    description=row[6],
                    merchant_id=row[7],
                    merchant_category=row[8],
                    status=row[9],
                    metadata=row[10] if isinstance(row[10], dict) else {}
                )

            offset += self.batch_size

        cursor.close()

    def _parse_transaction(self, data: Dict[str, Any]) -> TransactionRecord:
        """Convierte diccionario de API a TransactionRecord."""
        return TransactionRecord(
            transaction_id=data["id"],
            account_id=data["account_id"],
            timestamp=datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00')),
            amount=float(data["amount"]),
            currency=data.get("currency", "USD"),
            transaction_type=data["type"],
            description=data.get("description", ""),
            merchant_id=data.get("merchant_id"),
            merchant_category=data.get("merchant_category"),
            status=data.get("status", "completed"),
            metadata=data.get("metadata", {})
        )

    def _row_to_transaction_record(self, row: pd.Series) -> TransactionRecord:
        """Convierte fila de DataFrame a TransactionRecord."""
        return TransactionRecord(
            transaction_id=str(row['transaction_id']),
            account_id=str(row['account_id']),
            timestamp=pd.to_datetime(row['timestamp']),
            amount=float(row['amount']),
            currency=str(row.get('currency', 'USD')),
            transaction_type=str(row['transaction_type']),
            description=str(row.get('description', '')),
            merchant_id=str(row['merchant_id']) if pd.notna(row.get('merchant_id')) else None,
            merchant_category=str(row['merchant_category']) if pd.notna(row.get('merchant_category')) else None,
            status=str(row.get('status', 'completed')),
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading bank transactions from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(start_date, end_date, account_ids)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "transactions")
            yield from self.read_from_s3(bucket, prefix, start_date, end_date)
        elif self.source_type == "database":
            yield from self.read_from_database(start_date, end_date, account_ids)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas para integración con el pipeline.
        """
        records = list(self.read(start_date, end_date, account_ids))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logger.info(f"Loaded {len(df)} transactions")

        return df

    def close(self):
        """Cleanup de recursos."""
        if self._db_connection:
            self._db_connection.close()
            self._db_connection = None
        logger.info("Bank transactions reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> BankTransactionsReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return BankTransactionsReader(config.get("bank_transactions", {}))