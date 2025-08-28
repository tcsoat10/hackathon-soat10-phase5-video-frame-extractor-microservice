from datetime import datetime
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="BaseEntity")

class BaseEntity:
    
    def __init__(self, id: str, created_at: datetime, updated_at: datetime, inactivated_at: datetime) -> None:
        self._id = id
        self._created_at = created_at
        self._updated_at = updated_at
        self._inactivated_at = inactivated_at
        
    # getters and setters
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime) -> None:
        self._created_at = value

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self._updated_at = value

    @property
    def inactivated_at(self) -> datetime:
        return self._inactivated_at

    @inactivated_at.setter
    def inactivated_at(self, value: datetime) -> None:
        self._inactivated_at = value

    @property
    def is_new(self) -> bool:
        return self.id is None
    
    @classmethod
    def from_json(cls: Type[T], json_data: Dict[str, Any]) -> T:
        return cls(**json_data)

    def soft_delete(self):
        self.inactivated_at = datetime.now()

    def is_deleted(self):
        return self.inactivated_at is not None
    
    def reactivate(self):
        self.inactivated_at = None
    
    def __repr__(self):
        attributes_dict = vars(self)
        attributes = ", ".join(
            f"{key.lstrip('_')}={value!r}" 
            for key, value in attributes_dict.items()
        )
        return f"{self.__class__.__name__}({attributes})"

__all__ = ["BaseEntity"]
