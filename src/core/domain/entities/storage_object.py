from typing import Optional

class StorageObject:
    """Representa um objeto já armazenado no Object Storage."""
    def __init__(self, bucket: str, key: str, url: str, metadata: Optional[dict] = None):
        self.bucket = bucket
        self.key = key
        self.url = url
        self.metadata = metadata or {}

__all__ = ["StorageObject"]
