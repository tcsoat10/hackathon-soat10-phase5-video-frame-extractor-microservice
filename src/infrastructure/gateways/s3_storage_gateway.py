from __future__ import annotations
from typing import List, Tuple, Optional
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from src.config.settings import LOG_LEVEL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_DEFAULT_REGION
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.domain.entities.storage_object import StorageObject
from src.core.domain.entities.storage_item import StorageItem
from src.core.domain.entities.storage_config import StorageConfig
from src.core.shared.logging_monitor_handler import LoggingMonitoringHandler


class S3StorageGateway(ObjectStorageGateway):
    """Concrete implementation of ObjectStorageGateway using AWS S3 (boto3).

    This implementation is synchronous and keeps responsibilities small:
    - translate boto3 responses into StorageObject
    - basic error handling
    - presigned url generation
    """

    def __init__(self, storage_config: StorageConfig = None) -> None:
        if not storage_config:
            storage_config = StorageConfig()
        
        config = Config(retries={"max_attempts": storage_config.max_attempts})

        client_kwargs = {"region_name": AWS_DEFAULT_REGION, "config": config}
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs.update({
                "aws_access_key_id": AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            })
            if AWS_SESSION_TOKEN:
                client_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

        self.logger = logging.getLogger("S3StorageGateway")
        self._client = boto3.client("s3", **client_kwargs)

        self.logger.debug("S3 client created; region=%s, creds_provided=%s, session_token=%s",
                          client_kwargs.get("region_name"),
                          bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY),
                          bool(AWS_SESSION_TOKEN))

        self._retry_attempts = int(storage_config.retry_attempts)
        self._retry_multiplier = float(storage_config.retry_multiplier)
        self._retry_min = int(storage_config.retry_min)
        self._retry_max = int(storage_config.retry_max)

        self.logger.setLevel(LOG_LEVEL)

        # console handler if no handlers are configured
        self._configure_logger(storage_config)

    def _configure_logger(self, storage_config: StorageConfig):        
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(LOG_LEVEL)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            
        if storage_config.monitoring_url:
            self.logger.addHandler(LoggingMonitoringHandler(url=storage_config.monitoring_url))



    def upload_object(self, item: StorageItem) -> StorageObject:
        """Upload a single StorageItem to S3 and return a StorageObject pointing to it."""
        try:
            params = {
                "Bucket": item.bucket,
                "Key": item.key,
                "Body": item.content,
            }
            if item.content_type:
                params["ContentType"] = item.content_type

            response = self._client.put_object(**params)

            metadata = {}
            if response is not None:
                etag = response.get("ETag")
                if etag:
                    metadata["ETag"] = etag

            url = self.presign_url(item.bucket, item.key)
            self.logger.info("Uploaded object %s/%s", item.bucket, item.key)
            return StorageObject(bucket=item.bucket, key=item.key, url=url, metadata=metadata)

        except ClientError as exc:
            aws_err = getattr(exc, "response", {}).get("Error", {})
            err_message = aws_err.get("Message") or str(exc)
            self.logger.error("Failed to upload object %s/%s: %s - %s", item.bucket, item.key, aws_err.get("Code"), err_message)
            raise

    def download_object(self, bucket: str, key: str) -> bytes:
        """Download an object from S3 and return its content as bytes."""
        try:
            response = self._client.get_object(Bucket=bucket, Key=key)
            content = response["Body"].read()
            self.logger.info("Downloaded object %s/%s", bucket, key)
            return content
        except ClientError as exc:
            self.logger.error("Failed to download object %s/%s: %s", bucket, key, exc)
            raise

    def upload_objects_bulk(
        self,
        items: List[Tuple[bytes, str]],
        bucket: str,
        prefix: str,
        content_type: Optional[str] = None,
    ) -> List[StorageObject]:
        """Upload multiple objects to S3 in bulk and return a list of StorageObjects."""
        storage_objects = []
        for content, key_suffix in items:
            key = f"{prefix.rstrip('/')}/{key_suffix}"
            item = StorageItem(bucket=bucket, key=key, content=content, content_type=content_type)
            storage_objects.append(self.upload_object(item))
        return storage_objects

    def presign_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        """Generate a presigned URL to access an object in S3."""
        try:
            url = self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as exc:
            self.logger.error("Failed to generate presigned URL for %s/%s: %s", bucket, key, exc)
            raise

    def list_objects(self, bucket: str, prefix: str, max_keys: int = 1000) -> List[StorageObject]:
        try:
            paginator = self._client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix, MaxKeys=max_keys)

            objects = []
            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        key = obj["Key"]
                        url = self.presign_url(bucket, key)
                        objects.append(StorageObject(bucket=bucket, key=key, url=url))
            return objects
        except ClientError as exc:
            self.logger.error("Failed to list objects in bucket %s with prefix %s: %s", bucket, prefix, exc)
            raise
            

    def delete_object(self, bucket: str, key: str) -> bool:
        try:
            self._client.delete_object(Bucket=bucket, Key=key)
            self.logger.info("Deleted object %s/%s", bucket, key)
            return True
        except ClientError as exc:
            self.logger.error("Failed to delete object %s/%s: %s", bucket, key, exc)
            return False

    def delete_prefix(self, bucket: str, prefix: str) -> int:
        try:
            objects_to_delete = self.list_objects(bucket, prefix)
            if not objects_to_delete:
                self.logger.info("No objects found to delete for prefix %s/%s", bucket, prefix)
                return 0

            delete_keys = [{"Key": obj.key} for obj in objects_to_delete]
            response = self._client.delete_objects(
                Bucket=bucket,
                Delete={"Objects": delete_keys, "Quiet": False}
            )
            deleted_count = len(response.get("Deleted", []))
            errors = response.get("Errors", [])
            if errors:
                for error in errors:
                    self.logger.error("Error deleting object %s/%s: %s", bucket, error.get("Key"), error.get("Message"))
            self.logger.info("Deleted %d objects from bucket %s with prefix %s", deleted_count, bucket, prefix)
            return deleted_count
        except ClientError as exc:
            self.logger.error("Failed to delete objects with prefix %s/%s: %s", bucket, prefix, exc)
            raise


__all__ = ["S3StorageGateway"]
