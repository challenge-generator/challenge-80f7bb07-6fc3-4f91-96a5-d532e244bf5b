"""Financial data transformation module for normalizing and enriching data."""

import logging
from typing import Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

from src.transform.data_quality_rules import (
    FinancialDataQualityRules,
    QualityRuleEngine,
    DataQualityRuleSet
)

logger = logging.getLogger(__name__)


class SchemaNormalizer:
    """Normalizes data schemas across different financial data sources."""
    
    def __init__(self, schema_path: str = "src/schemas"):
        self.schema_path = Path(schema_path)
        self.schemas: dict[str, dict] = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load JSON schemas from the schema directory."""
        schema_files = ["transaction_schema.json", "market_data_schema.json", "news_schema.json"]
        
        for schema_file in schema_files:
            schema_file_path = self.schema_path / schema_file
            if schema_file_path.exists():
                with open(schema_file_path, 'r') as f:
                    schema_name = schema_file.replace("_schema.json", "")
                    self.schemas[schema_name] = json.load(f)
                    logger.info(f"Loaded schema: {schema_name}")
    
    def normalize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize transaction data to standard schema."""
        normalized = df.copy()
        
        if "transaction_id" in normalized.columns and "id" in normalized.columns:
            normalized = normalized.drop(columns=["id"])
        
        if "txn_amount" in normalized.columns and "amount" not in normalized.columns:
            normalized.rename(columns={"txn_amount": "amount"}, inplace=True)
        
        if "txn_date" in normalized.columns and "timestamp" not in normalized.columns:
            normalized.rename(columns={"txn_date": "timestamp"}, inplace=True)
        
        if "txn_type" in normalized.columns and "transaction_type" not in normalized.columns:
            normalized.rename(columns={"txn_type": "transaction_type"}, inplace=True)
        
        required_columns = ["transaction_id", "amount", "timestamp", "currency", "account_id"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "bank_transactions"
        
        return normalized[required_columns + ["transaction_type", "ingestion_timestamp", "data_source"]]
    
    def normalize_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize market data to standard schema."""
        normalized = df.copy()
        
        if "ticker" in normalized.columns and "symbol" not in normalized.columns:
            normalized.rename(columns={"ticker": "symbol"}, inplace=True)
        
        if "close_price" in normalized.columns and "price" not in normalized.columns:
            normalized.rename(columns={"close_price": "price"}, inplace=True)
        
        if "trade_date" in normalized.columns and "timestamp" not in normalized.columns:
            normalized.rename(columns={"trade_date": "timestamp"}, inplace=True)
        
        required_columns = ["symbol", "price", "timestamp"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        if "volume" not in normalized.columns:
            normalized["volume"] = 0
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "market_data"
        
        return normalized[required_columns + ["volume", "ingestion_timestamp", "data_source"]]
    
    def normalize_news(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize financial news to standard schema."""
        normalized = df.copy()
        
        if "title" in normalized.columns and "headline" not in normalized.columns:
            normalized.rename(columns={"title": "headline"}, inplace=True)
        
        if "pub_date" in normalized.columns and "published_at" not in normalized.columns:
            normalized.rename(columns={"pub_date": "published_at"}, inplace=True)
        
        if "news_source" in normalized.columns and "source" not in normalized.columns:
            normalized.rename(columns={"news_source": "source"}, inplace=True)
        
        required_columns = ["headline", "published_at"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        if "source" not in normalized.columns:
            normalized["source"] = "unknown"
        
        if "sentiment_score" not in normalized.columns:
            normalized["sentiment_score"] = None
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "financial_news"
        
        return normalized[required_columns + ["source", "sentiment_score", "ingestion_timestamp", "data_source"]]


class FinancialMetricsCalculator:
    """Calculate derived financial metrics from normalized data."""
    
    @staticmethod
    def calculate_transaction_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for transaction data."""
        result = df.copy()
        
        result["abs_amount"] = result["amount"].abs()
        
        result["is_credit"] = result["amount"] > 0
        result["is_debit"] = result["amount"] < 0
        
        result["day_of_week"] = pd.to_datetime(result["timestamp"]).dt.dayofweek
        result["month"] = pd.to_datetime(result["timestamp"]).dt.month
        result["year"] = pd.to_datetime(result["timestamp"]).dt.year
        
        result["amount_bucket"] = pd.cut(
            result["abs_amount"],
            bins=[0, 100, 1000, 10000, 100000, float('inf')],
            labels=["micro", "small", "medium", "large", "xlarge"]
        )
        
        return result
    
    @staticmethod
    def calculate_market_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for market data."""
        result = df.copy()
        
        result = result.sort_values(["symbol", "timestamp"])
        
        result["price_change"] = result.groupby("symbol")["price"].diff()
        result["price_change_pct"] = result.groupby("symbol")["price"].pct_change() * 100
        
        result["moving_avg_5d"] = result.groupby("symbol")["price"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        
        result["volatility_5d"] = result.groupby("symbol")["price"].transform(
            lambda x: x.rolling(window=5, min_periods=1).std()
        )
        
        result["volume_ma_5d"] = result.groupby("symbol")["volume"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        
        return result
    
    @staticmethod
    def calculate_news_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for news data."""
        result = df.copy()
        
        result["headline_length"] = result["headline"].str.len()
        
        result["published_hour"] = pd.to_datetime(result["published_at"]).dt.hour
        result["published_day_of_week"] = pd.to_datetime(result["published_at"]).dt.dayofweek
        
        result["sentiment_category"] = pd.cut(
            result["sentiment_score"],
            bins=[-1.0, -0.3, 0.3, 1.0],
            labels=["negative", "neutral", "positive"]
        )
        
        return result


class DataTransformer:
    """Main transformer orchestrating normalization and metric calculation."""
    
    def __init__(self, schema_path: str = "src/schemas"):
        self.normalizer = SchemaNormalizer(schema_path)
        self.metrics_calculator = FinancialMetricsCalculator()
        self.quality_engine = QualityRuleEngine()
        
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_transaction_rules())
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_market_data_rules())
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_news_rules())
    
    def transform_transactions(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform transaction data through the full pipeline."""
        logger.info(f"Transforming {len(df)} transactions")
        
        normalized = self.normalizer.normalize_transactions(df)
        logger.info(f"Normalized transactions schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_transaction_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("bank_transactions", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }
    
    def transform_market_data(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform market data through the full pipeline."""
        logger.info(f"Transforming {len(df)} market data records")
        
        normalized = self.normalizer.normalize_market_data(df)
        logger.info(f"Normalized market data schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_market_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("market_data", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }
    
    def transform_news(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform financial news through the full pipeline."""
        logger.info(f"Transforming {len(df)} news articles")
        
        normalized = self.normalizer.normalize_news(df)
        logger.info(f"Normalized news schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_news_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("financial_news", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }