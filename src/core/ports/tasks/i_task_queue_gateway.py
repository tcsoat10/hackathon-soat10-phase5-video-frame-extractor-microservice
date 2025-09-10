from abc import ABC, abstractmethod
from typing import Dict, Any

class ITaskQueueGateway(ABC):
    @abstractmethod
    def enqueue_video_processing_task(self, task_data: Dict[str, Any]) -> str:
        """Enfileira uma tarefa de processamento de vídeo."""
        pass

__all__ = ["ITaskQueueGateway"]
