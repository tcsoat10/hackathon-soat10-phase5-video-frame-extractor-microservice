from typing import IO, Any, Optional

class StorageItem:
    """
    Representa um item a ser enviado para o Object Storage.

    Parâmetros:
    - bucket (str): O nome do bucket no Object Storage.
    - key (str): O caminho do objeto no bucket.
    - content (Optional[bytes]): O conteúdo do objeto em bytes. (Deprecated: use file_object instead)
    - content_type (Optional[str]): O tipo de conteúdo (MIME type) do objeto.
    - file_object (Optional[IO[Any]]): Um objeto de arquivo (ex: BytesIO, SpooledTemporaryFile) para streaming.
    """
    def __init__(
        self,
        bucket: str,
        key: str,
        content: Optional[bytes] = None,
        content_type: Optional[str] = None,
        file_object: Optional[IO[Any]] = None,
    ):
        self.bucket = bucket
        self.key = key

        self.content = content  # deprecated: use file_object instead.

        self.file_object = file_object
        self.content_type = content_type

__all__ = ["StorageItem"]
