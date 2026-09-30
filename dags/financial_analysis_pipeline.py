"""
DAG principal para el pipeline de análisis financiero.
Orquesta las etapas de extracción, transformación y carga de datos
provenientes de múltiples fuentes: transacciones bancarias, datos de mercado y noticias financieras.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor

import pandas as pd
import boto3
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

ENVIRONMENT = Variable.get('environment', default_var='dev')
EXECUTION_DATE = '{{ ds }}'


def load_config() -> Dict[str, Any]:
    """Carga la configuración del pipeline según el ambiente."""
    config_path = f'conf/{ENVIRONMENT}_config.json'
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config {config_path} no encontrada, usando defaults")
        return {
            's3_bucket': 'financial-data-platform',
            'data_lake_path': 's3://financial-data-platform/data-lake/',
            'output_path': 's3://financial-data-platform/output/',
            'quality_threshold': 0.95,
            'batch_size': 10000
        }


def extract_bank_transactions(**context) -> str:
    """Extrae datos de transacciones bancarias desde la fuente origen."""
    from src.extract.bank_transactions_reader import BankTransactionsReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de transacciones bancarias para {execution_date}")
    
    reader = BankTransactionsReader(
        s3_bucket=config.get('s3_bucket'),
        region_name=config.get('aws_region', 'us-east-1')
    )
    
    transactions = reader.read(
        start_date=execution_date,
        end_date=execution_date,
        account_ids=config.get('account_ids', [])
    )
    
    output_key = f"raw/bank_transactions/{execution_date}/transactions.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(transactions)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídas {len(transactions)} transacciones bancarias")
    return output_key


def extract_market_data(**context) -> str:
    """Extrae datos de mercado financiero desde APIs externas."""
    from src.extract.market_data_reader import MarketDataReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de datos de mercado para {execution_date}")
    
    reader = MarketDataReader(
        api_key=config.get('market_api_key'),
        region=config.get('aws_region', 'us-east-1')
    )
    
    market_data = reader.read(
        symbols=config.get('market_symbols', ['AAPL', 'GOOGL', 'MSFT']),
        date=execution_date
    )
    
    output_key = f"raw/market_data/{execution_date}/market_data.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(market_data)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídos {len(market_data)} registros de mercado")
    return output_key


def extract_financial_news(**context) -> str:
    """Extrae noticias financieras desde fuentes de terceros."""
    from src.extract.financial_news_reader import FinancialNewsReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de noticias financieras para {execution_date}")
    
    reader = FinancialNewsReader(
        api_key=config.get('news_api_key'),
        region=config.get('aws_region', 'us-east-1')
    )
    
    news = reader.read(
        keywords=config.get('news_keywords', ['finance', 'stock', 'market']),
        date=execution_date
    )
    
    output_key = f"raw/financial_news/{execution_date}/news.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(news)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídas {len(news)} noticias financieras")
    return output_key


def validate_data_quality(**context) -> Dict[str, Any]:
    """Aplica reglas de calidad de datos a los datos extraídos."""
    from src.transform.data_quality_rules import DataQualityRules
    
    config = load_config()
    ti = context['ti']
    
    bank_transactions_key = ti.xcom_pull(task_ids='extract_bank_transactions')
    market_data_key = ti.xcom_pull(task_ids='extract_market_data')
    financial_news_key = ti.xcom_pull(task_ids='extract_financial_news')
    
    logger.info("Iniciando validación de calidad de datos")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    quality_rules = DataQualityRules(threshold=config.get('quality_threshold', 0.95))
    
    quality_results = {}
    
    for source, key in [
        ('bank_transactions', bank_transactions_key),
        ('market_data', market_data_key),
        ('financial_news', financial_news_key)
    ]:
        if key:
            obj = s3_hook.get_key(key, bucket)
            df = pd.read_parquet(f"s3://{bucket}/{key}")
            
            quality_result = quality_rules.validate(df, source)
            quality_results[source] = quality_result
            
            logger.info(f"Calidad {source}: {quality_result['score']:.2%}")
            
            if quality_result['score'] < config.get('quality_threshold', 0.95):
                quarantine_key = f"quarantine/{source}/{context['ds']}/data.parquet"
                buffer = df.to_parquet(engine='pyarrow', compression='snappy')
                s3_hook.load_bytes(
                    buffer.getvalue(),
                    key=quarantine_key,
                    bucket_name=bucket,
                    replace=True
                )
                logger.warning(f"Datos de {source} en cuarentena: score={quality_result['score']:.2%}")
    
    return json.dumps(quality_results)


def transform_financial_data(**context) -> str:
    """Aplica transformaciones financieras a los datos validados."""
    from src.transform.financial_data_transformer import FinancialDataTransformer
    
    config = load_config()
    ti = context['ti']
    
    bank_transactions_key = ti.xcom_pull(task_ids='extract_bank_transactions')
    market_data_key = ti.xcom_pull(task_ids='extract_market_data')
    financial_news_key = ti.xcom_pull(task_ids='extract_financial_news')
    
    logger.info("Iniciando transformación de datos financieros")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    transformer = FinancialDataTransformer(config)
    
    dfs = {}
    for source, key in [
        ('transactions', bank_transactions_key),
        ('market', market_data_key),
        ('news', financial_news_key)
    ]:
        if key:
            obj = s3_hook.get_key(key, bucket)
            dfs[source] = pd.read_parquet(f"s3://{bucket}/{key}")
    
    transformed_data = transformer.transform(dfs)
    
    output_key = f"transformed/financial_analysis/{context['ds']}/data.parquet"
    
    df = pd.DataFrame(transformed_data)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=bucket,
        replace=True
    )
    
    logger.info(f"Transformados {len(transformed_data)} registros")
    return output_key


def load_to_destination(**context) -> str:
    """Carga los datos transformados al destino final."""
    from src.load.data_writer import DataWriter
    
    config = load_config()
    ti = context['ti']
    
    transformed_key = ti.xcom_pull(task_ids='transform_financial_data')
    quality_results = ti.xcom_pull(task_ids='validate_data_quality')
    
    logger.info("Iniciando carga de datos al destino")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    obj = s3_hook.get_key(transformed_key, bucket)
    df = pd.read_parquet(f"s3://{bucket}/{transformed_key}")
    
    writer = DataWriter(
        output_path=config.get('output_path'),
        partition_by=['date', 'source'],
        format='delta'
    )
    
    result = writer.write(
        df=df,
        table_name='financial_analysis',
        mode='merge',
        partition_date=context['ds']
    )
    
    logger.info(f"Cargados {result['records_written']} registros a destino")
    return json.dumps(result)


def generate_analysis_report(**context):
    """Genera reporte de análisis y métricas del pipeline."""
    config = load_config()
    ti = context['ti']
    
    load_result = json.loads(ti.xcom_pull(task_ids='load_to_destination'))
    quality_results = json.loads(ti.xcom_pull(task_ids='validate_data_quality'))
    
    report = {
        'execution_date': context['ds'],
        'records_processed': load_result.get('records_written', 0),
        'quality_scores': quality_results,
        'status': 'SUCCESS' if load_result.get('records_written', 0) > 0 else 'FAILED',
        'environment': ENVIRONMENT
    }
    
    logger.info(f"Reporte de análisis: {json.dumps(report, indent=2)}")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    report_key = f"reports/{context['ds']}/analysis_report.json"
    
    s3_hook.load_string(
        json.dumps(report, indent=2),
        key=report_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    return report_key


with DAG(
    dag_id='financial_analysis_pipeline',
    default_args=DEFAULT_ARGS,
    description='Pipeline ETL para análisis financiero con datos de múltiples fuentes',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'financial', 'analysis', 'data-lake'],
    doc_md="""
# Pipeline de Análisis Financiero

Este DAG orquesta el flujo completo de extracción, transformación y carga de datos
provenientes de tres fuentes principales:
- Transacciones bancarias
- Datos de mercado financiero
- Noticias financieras

## Flujo de Ejecución

1. **Extracción**: Los datos se extraen de sus fuentes originales y se almacenan en formato Parquet.
2. **Validación**: Se aplican reglas de calidad para verificar integridad de los datos.
3. **Transformación**: Transformaciones financieras específicas se aplican a los datos validados.
4. **Carga**: Los datos transformados se cargan al destino final en formato Delta.
5. **Reporte**: Se genera un reporte de análisis del pipeline.

## Configuración

- **Programación**: Diario a las 6:00 AM
- **Retries**: 3 intentos con backoff exponencial
- **Particionamiento**: Por fecha y fuente de datos
"""
) as dag:
    
    start = EmptyOperator(task_id='start', doc_md='Inicio del pipeline de análisis financiero')
    
    extract_bank = PythonOperator(
        task_id='extract_bank_transactions',
        python_callable=extract_bank_transactions,
        provide_context=True,
        doc_md='Extrae transacciones bancarias desde la fuente origen'
    )
    
    extract_market = PythonOperator(
        task_id='extract_market_data',
        python_callable=extract_market_data,
        provide_context=True,
        doc_md='Extrae datos de mercado desde APIs externas'
    )
    
    extract_news = PythonOperator(
        task_id='extract_financial_news',
        python_callable=extract_financial_news,
        provide_context=True,
        doc_md='Extrae noticias financieras desde fuentes de terceros'
    )
    
    extraction_complete = EmptyOperator(
        task_id='extraction_complete',
        doc_md='Todas las fuentes de datos extraídas'
    )
    
    validate_quality = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
        doc_md='Aplica reglas de calidad a los datos extraídos',
        trigger_rule='all_done'
    )
    
    transform_data = PythonOperator(
        task_id='transform_financial_data',
        python_callable=transform_financial_data,
        provide_context=True,
        doc_md='Aplica transformaciones financieras a los datos validados',
        trigger_rule='all_done'
    )
    
    load_data = PythonOperator(
        task_id='load_to_destination',
        python_callable=load_to_destination,
        provide_context=True,
        doc_md='Carga los datos transformados al destino final',
        trigger_rule='all_done'
    )
    
    generate_report = PythonOperator(
        task_id='generate_analysis_report',
        python_callable=generate_analysis_report,
        provide_context=True,
        doc_md='Genera reporte de análisis y métricas del pipeline',
        trigger_rule='all_done'
    )
    
    end = EmptyOperator(task_id='end', doc_md='Fin del pipeline de análisis financiero')
    
    start >> [extract_bank, extract_market, extract_news] >> extraction_complete
    extraction_complete >> validate_quality >> transform_data >> load_data >> generate_report >> end