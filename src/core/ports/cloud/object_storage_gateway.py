from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.core.domain.entities.storage_object import StorageObject
from src.core.domain.entities.storage_item import StorageItem

class ObjectStorageGateway(ABC):
    """
    Interface storage bucket
    """
    @abstractmethod
    def upload_object(self, item: StorageItem) -> StorageObject:
        """Upload to bucket -> recebe um `StorageItem` e retorna um `StorageObject`"""
        pass

    @abstractmethod
    def download_object(self, bucket: str, key: str) -> bytes:
        """Download genérico"""
        pass

    @abstractmethod
    def upload_objects_bulk(
        self,
        items: List[Tuple[bytes, str]],
        bucket: str,
        prefix: str,
        content_type: Optional[str] = None
    ) -> List[StorageObject]:
        """Upload em lote: lista de (bytes, key_suffix) -> retorna StorageObject por item"""
        pass

    @abstractmethod
    def presign_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        """Gera URL pré-assinada para GET"""
        pass

    @abstractmethod
    def list_objects(self, bucket: str, prefix: str, max_keys: int = 1000) -> List[StorageObject]:
        """Lista objetos sob um prefix -> retorna lista de `StorageObject`"""
        pass

    @abstractmethod
    def delete_object(self, bucket: str, key: str) -> bool:
        """Deleta um objeto"""
        pass

    @abstractmethod
    def delete_prefix(self, bucket: str, prefix: str) -> int:
        """Deleta todos os objetos sob um prefix. Retorna quantidade deletada."""
        pass
