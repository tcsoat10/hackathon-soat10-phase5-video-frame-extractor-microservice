from typing import Any, Dict, List, Type, TypeVar, Generic

from src.core.domain.entities.base_entity import T

D = TypeVar("D")

class DTOPresenter(Generic[T, D]):

    @staticmethod
    def transform(entity: T, dto_class: Type[D]) -> D:
        return dto_class.from_entity(entity)

    @staticmethod
    def transform_list(entities: List[T], dto_class: Type[D]) -> List[D]:
        return [DTOPresenter.transform(entity, dto_class) for entity in entities]
    
    @staticmethod
    def transform_from_dict(data: Dict[str, Any], dto_class: Type[D]) -> D:
        return dto_class.from_dict(data)
