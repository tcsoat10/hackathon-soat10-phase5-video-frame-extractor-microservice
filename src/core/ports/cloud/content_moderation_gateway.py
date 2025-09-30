from abc import ABC, abstractmethod
from typing import Dict, Any

class ContentModerationGateway(ABC):
    """
    Interface para moderação de conteúdo de vídeo
    """
    
    @abstractmethod
    def moderate_video_content(self, bucket: str, video_key: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo de um vídeo para detectar conteúdo inadequado
        
        Args:
            bucket: Nome do bucket S3 onde está o vídeo
            video_key: Chave/path do vídeo no S3
            
        Returns:
            Dict contendo informações sobre a moderação:
            {
                "is_appropriate": bool,
                "confidence": float,
                "labels": List[str],
                "job_id": str
            }
        """
        pass