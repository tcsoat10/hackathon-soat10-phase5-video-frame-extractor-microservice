import os
from pathlib import Path
from typing import List, Tuple, Optional
from src.core.domain.entities.storage_item import StorageItem 
from src.core.domain.entities.storage_object import StorageObject
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway


class LocalObjectStorageGateway(ObjectStorageGateway):
    """
    Gateway de armazenamento de objetos que simula um bucket S3 local.
    """
    def __init__(self):
        self.base_path = Path('./bucket')
        self.base_path.mkdir(parents=True, exist_ok=True)
        print(f"Usando armazenamento local em: {self.base_path.resolve()}")

    def _get_full_path(self, bucket: str, key: str) -> Path:
        safe_key = (key or "").lstrip("/")
        full_path = (self.base_path / bucket / safe_key)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path = full_path.resolve()

        base_resolved = self.base_path.resolve()
        if not str(full_path).startswith(str(base_resolved)):
            raise ValueError("Key inválida: tentativa de acessar caminho fora do bucket")

        return full_path

    def upload_object(self, item: StorageItem) -> StorageObject:
        full_path = self._get_full_path(item.bucket, item.key)
        with open(full_path, "wb") as f:
            f.write(item.content)
        
        return StorageObject(
            bucket=item.bucket,
            key=item.key,
            url=str(full_path.resolve())
        )

    def download_object(self, bucket: str, key: str) -> bytes:
        full_path = self._get_full_path(bucket, key)
        print(f'Bucket PATH: {full_path}')
        if not full_path.exists():
            raise FileNotFoundError(f"Objeto não encontrado em {full_path}")
        
        with open(full_path, "rb") as f:
            return f.read()

    def upload_objects_bulk(self, items: List[Tuple[bytes, str]], bucket: str, prefix: str, content_type: Optional[str] = None) -> List[StorageObject]:
        storage_objects = []
        for content, key_suffix in items:
            key = f"{prefix.rstrip('/')}/{key_suffix}"
            item = StorageItem(bucket=bucket, key=key, content=content, content_type=content_type)
            storage_objects.append(self.upload_object(item))
        return storage_objects

    def presign_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        return f"file://{self._get_full_path(bucket, key).resolve()}"

    def list_objects(self, bucket: str, prefix: str, max_keys: int = 1000) -> List[StorageObject]:
        bucket_path = self.base_path / bucket
        prefix_path = bucket_path / prefix
        objects = []
        for file_path in prefix_path.rglob('*'):
            if file_path.is_file():
                key = str(file_path.relative_to(bucket_path))
                objects.append(StorageObject(bucket=bucket, key=key, url=str(file_path.resolve())))
                if len(objects) >= max_keys:
                    break
        return objects

    def delete_object(self, bucket: str, key: str) -> bool:
        path = self._get_full_path(bucket, key)
        if path.exists():
            path.unlink()
            return True
        return False
        
    def delete_prefix(self, bucket: str, prefix: str) -> int:
        bucket_path = self.base_path / bucket
        prefix_path = bucket_path / prefix
        deleted_count = 0
        if prefix_path.exists():
            if prefix_path.is_file():
                prefix_path.unlink()
                deleted_count = 1
            else:
                for file_path in prefix_path.rglob('*'):
                    if file_path.is_file():
                        file_path.unlink()
                        deleted_count += 1
        return deleted_count

__all__ = ["LocalObjectStorageGateway"]
