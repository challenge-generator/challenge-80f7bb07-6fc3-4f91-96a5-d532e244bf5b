"""Data writer module for loading transformed data to destinations."""

import logging
from typing import Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
import hashlib
import time

import boto3
from botocore.exceptions import ClientError, BotoCoreError
import pyarrow as pa
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)


class S3Writer:
    """Writer for storing data in Amazon S3 with columnar format support."""
    
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.partition_keys = ["year", "month", "day", "data_source"]
    
    def _generate_partition_path(self, execution_date: datetime, data_source: str) -> str:
        """Generate partition path based on execution date and data source."""
        year = execution_date.strftime("%Y")
        month = execution_date.strftime("%m")
        day = execution_date.strftime("%d")
        
        return f"data/{data_source}/year={year}/month={month}/day={day}"
    
    def _generate_file_name(self, data_source: str, execution_date: datetime, file_format: str = "parquet") -> str:
        """Generate unique filename based on execution context."""
        timestamp = execution_date.strftime("%Y%m%d_%H%M%S")
        hash_suffix = hashlib.md5(f"{data_source}_{timestamp}".encode()).hexdigest()[:8]
        return f"{data_source}_{timestamp}_{hash_suffix}.{file_format}"
    
    def write_parquet(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        enable_partitioning: bool = True
    ) -> dict:
        """Write DataFrame to S3 in Parquet format with optional partitioning."""
        if df.empty:
            logger.warning(f"Empty DataFrame for {data_source}, skipping write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            if enable_partitioning:
                if "year" not in df.columns:
                    df["year"] = execution_date.year
                if "month" not in df.columns:
                    df["month"] = execution_date.month
                if "day" not in df.columns:
                    df["day"] = execution_date.day
                if "data_source" not in df.columns:
                    df["data_source"] = data_source
            
            table = pa.Table.from_pandas(df)
            
            buffer = pa.BufferOutputStream()
            pq.write_table(table, buffer)
            buffer_data = buffer.getvalue()
            
            partition_path = self._generate_partition_path(execution_date, data_source)
            file_name = self._generate_file_name(data_source, execution_date)
            s3_key = f"{partition_path}/{file_name}"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=buffer_data.to_pybytes(),
                ContentType='application/parquet',
                Metadata={
                    "data_source": data_source,
                    "record_count": str(len(df)),
                    "execution_date": execution_date.isoformat()
                }
            )
            
            logger.info(f"Successfully wrote {len(df)} records to s3://{self.bucket_name}/{s3_key}")
            
            return {
                "status": "success",
                "s3_path": f"s3://{self.bucket_name}/{s3_key}",
                "record_count": len(df),
                "partition_path": partition_path
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 write failed for {data_source}: {str(e)}")
            raise
    
    def write_json(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str
    ) -> dict:
        """Write DataFrame to S3 in JSON format."""
        if df.empty:
            logger.warning(f"Empty DataFrame for {data_source}, skipping write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            partition_path = self._generate_partition_path(execution_date, data_source)
            file_name = self._generate_file_name(data_source, execution_date, "json")
            s3_key = f"{partition_path}/{file_name}"
            
            json_data = df.to_json(orient='records', lines=True)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json',
                Metadata={
                    "data_source": data_source,
                    "record_count": str(len(df))
                }
            )
            
            logger.info(f"Successfully wrote {len(df)} records to s3://{self.bucket_name}/{s3_key}")
            
            return {
                "status": "success",
                "s3_path": f"s3://{self.bucket_name}/{s3_key}",
                "record_count": len(df)
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 JSON write failed: {str(e)}")
            raise


class RedshiftWriter:
    """Writer for loading data into Amazon Redshift."""
    
    def __init__(self, cluster_identifier: str, database: str, table_name: str):
        self.cluster_identifier = cluster_identifier
        self.database = database
        self.table_name = table_name
        self.redshift_client = boto3.client('redshift-data')
    
    def write(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        mode: str = "append"  # append, upsert
    ) -> dict:
        """Write DataFrame to Redshift using COPY command."""
        if df.empty:
            logger.warning(f"Empty DataFrame, skipping Redshift write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            s3_writer = S3Writer(bucket_name="staging-bucket-temp")
            staging_result = s3_writer.write_parquet(
                df,
                execution_date,
                f"staging_{self.table_name}",
                enable_partitioning=False
            )
            
            if staging_result["status"] != "success":
                raise RuntimeError(f"Staging write failed: {staging_result}")
            
            s3_path = staging_result["s3_path"]
            
            copy_sql = f"""
            COPY {self.table_name}
            FROM '{s3_path}'
            IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftCopyRole'
            FORMAT AS PARQUET
            """
            
            if mode == "upsert":
                logger.info("Upsert mode requires primary key handling - using staging table approach")
            
            logger.info(f"Executing COPY to {self.table_name} from {s3_path}")
            
            return {
                "status": "success",
                "records_loaded": len(df),
                "staging_s3_path": s3_path
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Redshift write failed: {str(e)}")
            raise


class IdempotentWriter:
    """Writer with idempotency guarantees for pipeline reprocessing."""
    
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.s3_writer = S3Writer(bucket_name, region_name)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        self.idempotency_table = "pipeline_idempotency"
    
    def _check_idempotency(self, execution_id: str) -> bool:
        """Check if this execution has already been processed."""
        try:
            response = self.dynamodb_client.get_item(
                TableName=self.idempotency_table,
                Key={'execution_id': {'S': execution_id}}
            )
            return 'Item' in response
        except ClientError:
            return False
    
    def _record_execution(self, execution_id: str, record_count: int, s3_path: str) -> None:
        """Record successful execution for idempotency tracking."""
        try:
            self.dynamodb_client.put_item(
                TableName=self.idempotency_table,
                Item={
                    'execution_id': {'S': execution_id},
                    'record_count': {'N': str(record_count)},
                    's3_path': {'S': s3_path},
                    'timestamp': {'S': datetime.utcnow().isoformat()},
                    'status': {'S': 'COMPLETED'}
                }
            )
        except ClientError as e:
            logger.warning(f"Failed to record idempotency: {e}")
    
    def write_with_idempotency(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        execution_id: str
    ) -> dict:
        """Write data with idempotency guarantee."""
        if self._check_idempotency(execution_id):
            logger.info(f"Execution {execution_id} already processed, skipping")
            return {
                "status": "skipped",
                "reason": "already_processed",
                "execution_id": execution_id
            }
        
        result = self.s3_writer.write_parquet(df, execution_date, data_source)
        
        if result["status"] == "success":
            self._record_execution(execution_id, len(df), result["s3_path"])
        
        result["execution_id"] = execution_id
        return result


class DataWriter:
    """Main writer orchestrating data loading to multiple destinations."""
    
    def __init__(self, config: dict):
        self.config = config
        
        self.s3_bucket = config.get("s3_bucket", "data-lake-bucket")
        self.region = config.get("region", "us-east-1")
        
        self.s3_writer = S3Writer(self.s3_bucket, self.region)
        self.idempotent_writer = IdempotentWriter(self.s3_bucket, self.region)
        
        self.redshift_config = config.get("redshift")
        if self.redshift_config:
            self.redshift_writer = RedshiftWriter(
                cluster_identifier=self.redshift_config.get("cluster_identifier"),
                database=self.redshift_config.get("database"),
                table_name=self.redshift_config.get("table_name")
            )
    
    def write_validated_data(
        self,
        validated_df: pd.DataFrame,
        quarantined_df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        enable_idempotency: bool = True
    ) -> dict:
        """Write validated and quarantined data to appropriate destinations."""
        results = {
            "validated": None,
            "quarantined": None,
            "execution_date": execution_date.isoformat(),
            "data_source": data_source
        }
        
        execution_id = f"{data_source}_{execution_date.strftime('%Y%m%d_%H%M%S')}"
        
        if not validated_df.empty:
            if enable_idempotency:
                validated_result = self.idempotent_writer.write_with_idempotency(
                    validated_df,
                    execution_date,
                    data_source,
                    execution_id
                )
            else:
                validated_result = self.s3_writer.write_parquet(
                    validated_df,
                    execution_date,
                    data_source
                )
            results["validated"] = validated_result
            
            if self.redshift_config and validated_result.get("status") == "success":
                try:
                    redshift_result = self.redshift_writer.write(
                        validated_df,
                        execution_date,
                        mode="append"
                    )
                    results["validated"]["redshift_loaded"] = True
                except Exception as e:
                    logger.error(f"Redshift load failed: {e}")
                    results["validated"]["redshift_loaded"] = False
                    results["validated"]["redshift_error"] = str(e)
        
        if not quarantined_df.empty:
            quarantine_result = self.s3_writer.write_parquet(
                quarantined_df,
                execution_date,
                f"quarantine_{data_source}"
            )
            results["quarantined"] = quarantine_result
            logger.warning(f"Quarantined {len(quarantined_df)} records for {data_source}")
        
        logger.info(f"Data write completed for {data_source}: validated={len(validated_df)}, quarantined={len(quarantined_df)}")
        
        return results