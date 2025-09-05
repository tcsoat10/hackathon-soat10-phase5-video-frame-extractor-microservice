from enum import Enum

class VideoJobStatus(Enum):
    PENDING = ("PENDING", "Waiting for processing")
    PROCESSING = ("PROCESSING", "Processing in progress")
    COMPLETED = ("COMPLETED", "Processing completed")
    ERROR = ("ERROR", "An error occurred during processing")
    
    @property
    def status(self) -> str:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]
    
    @classmethod
    def status_and_descriptions(cls):
        """
        Retorna todos os valores e descrições dos métodos do Job Video.
        :return: Lista de dicionários com o status e descrição dos métodos.
        """
        return [{"status": status.status, "description": status.description} for status in cls]
    
    @classmethod
    def method_list(cls):
        """
        Retorna todos os status dos métodos do Job Video.
        :return: Lista de status dos métodos.
        """
        return [member.status for member in cls]
    
    @classmethod
    def to_dict(cls):
        """
        Retorna um dicionário mapeando os status dos métodos às suas descrições.
        :return: Dicionário com o status como chave e a descrição como valor.
        """
        return {member.status: member.description for member in cls}
    
    def __str__(self) -> str:
        return self.status
    
    def __repr__(self) -> str:
        return self.status


__all__ = ["VideoJobStatus"]
