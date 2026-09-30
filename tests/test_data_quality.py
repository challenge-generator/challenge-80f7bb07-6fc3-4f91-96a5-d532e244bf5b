import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.transform.data_quality_rules import (
    DataQualityValidator,
    QualityThreshold,
    QualityRule,
    ValidationResult
)


class TestDataQualityValidator:
    """Casos de prueba para validar las reglas de calidad de datos."""

    @pytest.fixture
    def sample_transactions_df(self):
        """DataFrame de transacciones bancarias de ejemplo."""
        data = {
            'transaction_id': ['TX001', 'TX002', 'TX003', 'TX004', 'TX005'],
            'account_id': ['ACC001', 'ACC002', 'ACC003', 'ACC004', 'ACC005'],
            'amount': [100.50, 250.00, -50.00, 1000.00, 75.25],
            'currency': ['USD', 'USD', 'EUR', 'USD', 'USD'],
            'transaction_date': [
                datetime(2024, 1, 15),
                datetime(2024, 1, 16),
                datetime(2024, 1, 17),
                datetime(2024, 1, 18),
                datetime(2024, 1, 19)
            ],
            'transaction_type': ['credit', 'debit', 'credit', 'credit', 'debit'],
            'status': ['completed', 'pending', 'completed', 'completed', 'failed']
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def quality_validator(self):
        """Instancia del validador con umbrales por defecto."""
        thresholds = {
            'null_percentage': 0.05,
            'duplicate_percentage': 0.02,
            'min_records': 10,
            'max_amount': 1000000.0,
            'min_amount': 0.01
        }
        return DataQualityValidator(thresholds)

    def test_validate_null_values_below_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que registros con valores nulos por debajo del umbral pasan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = np.nan
        
        result = quality_validator.validate_null_values(df, 'amount')
        
        assert result.is_valid is True
        assert result.null_count == 1
        assert result.null_percentage < 0.05

    def test_validate_null_values_above_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que registros con valores nulos por encima del umbral fallan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0:2, 'amount'] = np.nan
        
        result = quality_validator.validate_null_values(df, 'amount')
        
        assert result.is_valid is False
        assert result.null_count == 3
        assert result.null_percentage >= 0.05

    def test_validate_duplicates_below_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que duplicados por debajo del umbral pasan la validación."""
        df = pd.concat([sample_transactions_df, sample_transactions_df.iloc[[0]]], ignore_index=True)
        
        result = quality_validator.validate_duplicates(df, 'transaction_id')
        
        assert result.is_valid is True
        assert result.duplicate_count == 1

    def test_validate_duplicates_above_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que duplicados por encima del umbral fallan la validación."""
        df = pd.concat([sample_transactions_df, sample_transactions_df], ignore_index=True)
        
        result = quality_validator.validate_duplicates(df, 'transaction_id')
        
        assert result.is_valid is False
        assert result.duplicate_count == 5

    def test_validate_amount_range_valid(self, quality_validator, sample_transactions_df):
        """Verifica que montos dentro del rango válido pasan la validación."""
        result = quality_validator.validate_amount_range(sample_transactions_df, 'amount')
        
        assert result.is_valid is True
        assert result.invalid_count == 0

    def test_validate_amount_range_with_outliers(self, quality_validator, sample_transactions_df):
        """Verifica que montos fuera del rango fallan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = 5000000.0
        df.loc[1, 'amount'] = -100.0
        
        result = quality_validator.validate_amount_range(df, 'amount')
        
        assert result.is_valid is False
        assert result.invalid_count == 2

    def test_validate_minimum_records(self, quality_validator, sample_transactions_df):
        """Verifica que se cumple el mínimo de registros requeridos."""
        result = quality_validator.validate_minimum_records(sample_transactions_df)
        
        assert result.is_valid is True

    def test_validate_minimum_records_below_minimum(self, quality_validator):
        """Verifica que se detecta cuando hay menos registros que el mínimo."""
        df = pd.DataFrame({'a': [1, 2, 3]})
        
        result = quality_validator.validate_minimum_records(df)
        
        assert result.is_valid is False

    def test_quarantine_invalid_records(self, quality_validator, sample_transactions_df):
        """Verifica que los registros inválidos se aíslan correctamente en cuarentena."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = np.nan
        df.loc[1, 'amount'] = -50.00
        df.loc[2, 'transaction_id'] = 'TX001'
        
        valid_df, quarantine_df = quality_validator.quarantine_invalid_records(df)
        
        assert len(quarantine_df) >= 3
        assert len(valid_df) <= 2

    def test_validate_currency_format(self, quality_validator):
        """Verifica la validación del formato de moneda."""
        data = {
            'currency': ['USD', 'EUR', 'GBP', 'INVALID', 'JPY']
        }
        df = pd.DataFrame(data)
        valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF']
        
        result = quality_validator.validate_currency_format(df, 'currency', valid_currencies)
        
        assert result.is_valid is False
        assert result.invalid_count == 1

    def test_validate_date_range(self, quality_validator, sample_transactions_df):
        """Verifica que las fechas estén dentro del rango válido."""
        df = sample_transactions_df.copy()
        df.loc[0, 'transaction_date'] = datetime(2020, 1, 1)
        
        min_date = datetime(2023, 1, 1)
        max_date = datetime(2025, 12, 31)
        
        result = quality_validator.validate_date_range(df, 'transaction_date', min_date, max_date)
        
        assert result.is_valid is False
        assert result.invalid_count == 1

    def test_comprehensive_quality_check(self, quality_validator, sample_transactions_df):
        """Verifica la ejecución de un chequeo completo de calidad."""
        results = quality_validator.run_comprehensive_check(sample_transactions_df)
        
        assert isinstance(results, dict)
        assert 'null_validation' in results
        assert 'duplicate_validation' in results
        assert 'amount_range_validation' in results
        assert 'min_records_validation' in results
        
        for key, result in results.items():
            assert isinstance(result, ValidationResult)


class TestQualityThreshold:
    """Casos de prueba para los umbrales de calidad."""

    def test_threshold_creation(self):
        """Verifica la correcta creación de un umbral."""
        threshold = QualityThreshold(
            name='null_percentage',
            value=0.05,
            operator='less_than'
        )
        
        assert threshold.name == 'null_percentage'
        assert threshold.value == 0.05
        assert threshold.operator == 'less_than'

    def test_threshold_evaluation_less_than(self):
        """Verifica la evaluación de umbral con operador less_than."""
        threshold = QualityThreshold('test', 0.1, 'less_than')
        
        assert threshold.evaluate(0.05) is True
        assert threshold.evaluate(0.15) is False

    def test_threshold_evaluation_greater_than(self):
        """Verifica la evaluación de umbral con operador greater_than."""
        threshold = QualityThreshold('test', 10, 'greater_than')
        
        assert threshold.evaluate(15) is True
        assert threshold.evaluate(5) is False

    def test_threshold_evaluation_equals(self):
        """Verifica la evaluación de umbral con operador equals."""
        threshold = QualityThreshold('test', 100, 'equals')
        
        assert threshold.evaluate(100) is True
        assert threshold.evaluate(50) is False


class TestQualityRule:
    """Casos de prueba para las reglas de calidad."""

    def test_rule_creation(self):
        """Verifica la correcta creación de una regla de calidad."""
        rule = QualityRule(
            name='no_null_transactions',
            description='No debe haber valores nulos en transaction_id',
            column='transaction_id',
            validation_type='not_null'
        )
        
        assert rule.name == 'no_null_transactions'
        assert rule.column == 'transaction_id'
        assert rule.validation_type == 'not_null'

    def test_custom_rule_execution(self):
        """Verifica la ejecución de una regla personalizada."""
        df = pd.DataFrame({'amount': [100, 200, -50, 300]})
        
        def negative_check(df, column):
            return df[column].min() >= 0
        
        rule = QualityRule(
            name='no_negative_amounts',
            description='Los montos no pueden ser negativos',
            column='amount',
            validation_type='custom',
            custom_validation=negative_check
        )
        
        result = rule.execute(df)
        
        assert result is False


class TestValidationResult:
    """Casos de prueba para el resultado de validación."""

    def test_validation_result_success(self):
        """Verifica la creación de un resultado exitoso."""
        result = ValidationResult(
            rule_name='test_rule',
            is_valid=True,
            message='Validación exitosa'
        )
        
        assert result.is_valid is True
        assert result.rule_name == 'test_rule'

    def test_validation_result_failure(self):
        """Verifica la creación de un resultado fallido."""
        result = ValidationResult(
            rule_name='test_rule',
            is_valid=False,
            message='Validación fallida',
            details={'failed_count': 5}
        )
        
        assert result.is_valid is False
        assert result.details['failed_count'] == 5