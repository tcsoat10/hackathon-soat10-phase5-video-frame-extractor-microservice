from typing import Optional

class StorageItem:
    """Representa um item a ser enviado para o Object Storage."""
    def __init__(self, bucket: str, key: str, content: bytes, content_type: Optional[str] = None):
        self.bucket = bucket
        self.key = key
        self.content = content
        self.content_type = content_type

__all__ = ["StorageItem"]
