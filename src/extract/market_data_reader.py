"""
Lector de datos de mercado para el pipeline de análisis financiero.
Extrae precios de acciones, divisas, commodities y otros instrumentos financieros.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class MarketDataType(Enum):
    """Tipos de datos de mercado soportados."""
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"
    CRYPTO = "crypto"
    INDEX = "index"
    BOND = "bond"


@dataclass
class MarketDataRecord:
    """Representa un registro de datos de mercado."""
    symbol: str
    timestamp: datetime
    data_type: MarketDataType
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    currency: str = "USD"
    exchange: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "data_type": self.data_type.value,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume,
            "currency": self.currency,
            "exchange": self.exchange,
            "metadata": self.metadata
        }


class MarketDataReader:
    """
    Clase principal para leer datos de mercado de múltiples fuentes.
    Soporta APIs de mercado, archivos históricos y streaming en tiempo real.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 500)
        self.max_retries = config.get("max_retries", 3)
        self._s3_client = None
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

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                wait_time = 2 * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def read_from_api(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> Iterator[MarketDataRecord]:
        """
        Lee datos de mercado desde API financiera (Bloomberg, Reuters, Alpha Vantage, etc.)
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
            "Content-Type": "application/json"
        }

        for symbol in symbols:
            params = {
                "symbol": symbol,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d"),
                "adjusted": "true",
                "outputsize": "full"
            }

            try:
                response = session.get(
                    f"{api_url}/time_series",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                for item in data.get("time_series", []):
                    yield self._parse_market_data(item, symbol, data_type)

            except requests.RequestException as e:
                logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
                continue

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[MarketDataRecord]:
        """
        Lee datos de mercado desde S3 con partición por símbolo y fecha.
        """
        s3_client = self._get_s3_client()

        for symbol in symbols:
            date_format = "%Y-%m-%d"
            date_range = pd.date_range(start_date, end_date, freq='D')

            for date_obj in date_range:
                date_str = date_obj.strftime(date_format)
                object_key = f"{prefix}/symbol={symbol}/date={date_str}/market_data.parquet"

                try:
                    response = s3_client.get_object(Bucket=bucket, Key=object_key)
                    data = response['Body'].read()

                    df = pd.read_parquet(pd.io.common.BytesIO(data))

                    for _, row in df.iterrows():
                        yield self._row_to_market_record(row, symbol)

                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code')
                    if error_code == 'NoSuchKey':
                        continue
                    logger.error(f"S3 error reading {object_key}: {str(e)}")
                    raise

    def read_historical_files(
        self,
        directory: str,
        symbols: Optional[List[str]] = None
    ) -> Iterator[MarketDataRecord]:
        """
        Lee archivos históricos locales o desde sistema de archivos mounting.
        """
        import os
        from pathlib import Path

        base_path = Path(directory)

        if not base_path.exists():
            logger.warning(f"Directory {directory} does not exist")
            return

        for file_path in base_path.rglob("*.parquet"):
            try:
                df = pd.read_parquet(file_path)

                for _, row in df.iterrows():
                    symbol = row.get('symbol', file_path.stem)
                    if symbols and symbol not in symbols:
                        continue
                    yield self._row_to_market_record(row, symbol)

            except Exception as e:
                logger.error(f"Error reading {file_path}: {str(e)}")
                continue

    def _parse_market_data(
        self,
        data: Dict[str, Any],
        symbol: str,
        data_type: MarketDataType
    ) -> MarketDataRecord:
        """Convierte respuesta de API a MarketDataRecord."""
        return MarketDataRecord(
            symbol=symbol,
            timestamp=datetime.fromisoformat(data["datetime"]),
            data_type=data_type,
            open_price=float(data["open"]),
            high_price=float(data["high"]),
            low_price=float(data["low"]),
            close_price=float(data["close"]),
            volume=float(data.get("volume", 0)),
            currency=data.get("currency", "USD"),
            exchange=data.get("exchange"),
            metadata=data.get("metadata", {})
        )

    def _row_to_market_record(self, row: pd.Series, symbol: str) -> MarketDataRecord:
        """Convierte fila de DataFrame a MarketDataRecord."""
        data_type_str = row.get('data_type', 'stock')
        try:
            data_type = MarketDataType(data_type_str)
        except ValueError:
            data_type = MarketDataType.STOCK

        return MarketDataRecord(
            symbol=symbol,
            timestamp=pd.to_datetime(row['timestamp']),
            data_type=data_type,
            open_price=float(row['open']),
            high_price=float(row['high']),
            low_price=float(row['low']),
            close_price=float(row['close']),
            volume=float(row.get('volume', 0)),
            currency=str(row.get('currency', 'USD')),
            exchange=str(row['exchange']) if pd.notna(row.get('exchange')) else None,
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> Iterator[MarketDataRecord]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading market data for {symbols} from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(symbols, start_date, end_date, data_type)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "market_data")
            yield from self.read_from_s3(bucket, prefix, symbols, start_date, end_date)
        elif self.source_type == "files":
            directory = self.source_credentials.get("data_directory")
            yield from self.read_historical_files(directory, symbols)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas.
        """
        records = list(self.read(symbols, start_date, end_date, data_type))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logger.info(f"Loaded {len(df)} market data records")

        return df

    def close(self):
        """Cleanup de recursos."""
        logger.info("Market data reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> MarketDataReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return MarketDataReader(config.get("market_data", {}))