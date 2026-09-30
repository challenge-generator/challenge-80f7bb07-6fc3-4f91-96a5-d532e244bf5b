"""Data quality rules and thresholds for financial data validation."""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class QualityThreshold:
    """Threshold configuration for a quality rule."""
    
    name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    null_percentage_allowed: float = 0.0
    unique_values_required: bool = False
    custom_validator: Optional[Callable[[Any], bool]] = None
    severity: str = "ERROR"  # ERROR, WARNING, INFO
    description: str = ""
    
    def validate(self, series: pd.Series) -> dict:
        """Validate a pandas Series against this threshold."""
        result = {
            "rule": self.name,
            "passed": True,
            "severity": self.severity,
            "details": {}
        }
        
        total_count = len(series)
        if total_count == 0:
            result["passed"] = False
            result["details"]["error"] = "Empty series"
            return result
        
        null_count = series.isnull().sum()
        null_percentage = (null_count / total_count) * 100
        
        if null_percentage > self.null_percentage_allowed:
            result["passed"] = False
            result["details"]["null_percentage"] = null_percentage
            result["details"]["null_threshold"] = self.null_percentage_allowed
        
        if self.min_value is not None:
            numeric_series = pd.to_numeric(series, errors='coerce')
            below_min = (numeric_series < self.min_value).sum()
            if below_min > 0:
                result["passed"] = False
                result["details"]["below_min_count"] = int(below_min)
                result["details"]["min_value"] = self.min_value
        
        if self.max_value is not None:
            numeric_series = pd.to_numeric(series, errors='coerce')
            above_max = (numeric_series > self.max_value).sum()
            if above_max > 0:
                result["passed"] = False
                result["details"]["above_max_count"] = int(above_max)
                result["details"]["max_value"] = self.max_value
        
        if self.unique_values_required:
            unique_count = series.nunique()
            if unique_count < total_count:
                result["passed"] = False
                result["details"]["unique_violations"] = int(total_count - unique_count)
        
        if self.custom_validator is not None:
            try:
                invalid_count = series.apply(lambda x: not self.custom_validator(x) if pd.notna(x) else False).sum()
                if invalid_count > 0:
                    result["passed"] = False
                    result["details"]["custom_validation_failures"] = int(invalid_count)
            except Exception as e:
                result["passed"] = False
                result["details"]["custom_validation_error"] = str(e)
        
        return result


@dataclass
class DataQualityRuleSet:
    """Collection of quality rules for a data source."""
    
    source_name: str
    rules: list[QualityThreshold] = field(default_factory=list)
    quarantine_threshold: float = 0.05  # 5% failure rate triggers quarantine
    
    def add_rule(self, rule: QualityThreshold) -> None:
        """Add a quality rule to the set."""
        self.rules.append(rule)
        logger.debug(f"Added rule '{rule.name}' to {self.source_name}")
    
    def validate_dataframe(self, df: pd.DataFrame) -> dict:
        """Validate a DataFrame against all rules in the set."""
        validation_results = {
            "source": self.source_name,
            "timestamp": datetime.utcnow().isoformat(),
            "total_rows": len(df),
            "rules_checked": len(self.rules),
            "passed": True,
            "results": [],
            "quarantine_required": False
        }
        
        failed_rules = 0
        
        for rule in self.rules:
            if rule.name not in df.columns:
                logger.warning(f"Column '{rule.name}' not found in DataFrame for source '{self.source_name}'")
                validation_results["results"].append({
                    "rule": rule.name,
                    "passed": False,
                    "severity": "ERROR",
                    "details": {"error": "Column not found"}
                })
                failed_rules += 1
                continue
            
            result = rule.validate(df[rule.name])
            validation_results["results"].append(result)
            
            if not result["passed"]:
                failed_rules += 1
                logger.warning(f"Quality rule '{rule.name}' failed for {self.source_name}: {result['details']}")
        
        failure_rate = failed_rules / len(self.rules) if self.rules else 0
        validation_results["failure_rate"] = failure_rate
        validation_results["failed_rules"] = failed_rules
        
        if failure_rate >= self.quarantine_threshold:
            validation_results["quarantine_required"] = True
            validation_results["passed"] = False
            logger.error(f"Quarantine required for {self.source_name}: {failure_rate*100:.2f}% failure rate")
        
        return validation_results


class FinancialDataQualityRules:
    """Predefined quality rules for financial data sources."""
    
    @staticmethod
    def get_transaction_rules() -> DataQualityRuleSet:
        """Get quality rules for bank transaction data."""
        rules = DataQualityRuleSet(source_name="bank_transactions")
        
        rules.add_rule(QualityThreshold(
            name="transaction_id",
            unique_values_required=True,
            severity="ERROR",
            description="Transaction ID must be unique"
        ))
        
        rules.add_rule(QualityThreshold(
            name="amount",
            min_value=-1000000,
            max_value=1000000,
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Transaction amount must be within reasonable bounds"
        ))
        
        rules.add_rule(QualityThreshold(
            name="timestamp",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Timestamp cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="currency",
            null_percentage_allowed=0.0,
            custom_validator=lambda x: x in ["USD", "EUR", "GBP", "JPY", "CHF"],
            severity="WARNING",
            description="Currency must be a supported code"
        ))
        
        rules.add_rule(QualityThreshold(
            name="account_id",
            null_percentage_allowed=0.0,
            unique_values_required=False,
            severity="ERROR",
            description="Account ID cannot be null"
        ))
        
        return rules
    
    @staticmethod
    def get_market_data_rules() -> DataQualityRuleSet:
        """Get quality rules for market data."""
        rules = DataQualityRuleSet(source_name="market_data")
        
        rules.add_rule(QualityThreshold(
            name="symbol",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Market symbol cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="price",
            min_value=0.01,
            max_value=1000000,
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Price must be positive and within bounds"
        ))
        
        rules.add_rule(QualityThreshold(
            name="volume",
            min_value=0,
            null_percentage_allowed=0.0,
            severity="WARNING",
            description="Volume cannot be negative"
        ))
        
        rules.add_rule(QualityThreshold(
            name="timestamp",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Timestamp cannot be null"
        ))
        
        return rules
    
    @staticmethod
    def get_news_rules() -> DataQualityRuleSet:
        """Get quality rules for financial news data."""
        rules = DataQualityRuleSet(source_name="financial_news")
        
        rules.add_rule(QualityThreshold(
            name="headline",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Headline cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="published_at",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Publication date cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="source",
            null_percentage_allowed=5.0,
            severity="WARNING",
            description="Source is optional but recommended"
        ))
        
        rules.add_rule(QualityThreshold(
            name="sentiment_score",
            min_value=-1.0,
            max_value=1.0,
            null_percentage_allowed=10.0,
            severity="WARNING",
            description="Sentiment score must be between -1 and 1"
        ))
        
        return rules


class QualityRuleEngine:
    """Engine to execute quality rules and manage quarantine logic."""
    
    def __init__(self):
        self.rule_sets: dict[str, DataQualityRuleSet] = {}
        self.quarantine_path = "s3://data-lake/quarantine/"
    
    def register_rule_set(self, rule_set: DataQualityRuleSet) -> None:
        """Register a rule set for a data source."""
        self.rule_sets[rule_set.source_name] = rule_set
        logger.info(f"Registered quality rules for source: {rule_set.source_name}")
    
    def validate(self, source_name: str, df: pd.DataFrame) -> dict:
        """Validate data against registered rules."""
        if source_name not in self.rule_sets:
            logger.warning(f"No rules registered for source: {source_name}")
            return {
                "source": source_name,
                "passed": True,
                "warning": "No validation rules applied"
            }
        
        rule_set = self.rule_sets[source_name]
        return rule_set.validate_dataframe(df)
    
    def get_quarantine_path(self, source_name: str, execution_date: datetime) -> str:
        """Generate quarantine path for failed records."""
        date_str = execution_date.strftime("%Y%m%d")
        return f"{self.quarantine_path}{source_name}/{date_str}/"