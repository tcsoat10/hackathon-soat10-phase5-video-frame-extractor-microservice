
from src.core.domain.entities.base_entity import BaseEntity

# pattern Identity Map - Martin Fowler
# https://martinfowler.com/eaaCatalog/identityMap.html
class IdentityMap:
    
    def __init__(self):
        self._entities = {}
        
    @classmethod
    def get_instance(cls) -> "IdentityMap":
        from src.core.containers import Container
        return Container.identity_map()
        
    def add(self, entity: BaseEntity):
        key = (entity.__class__, entity.id)
        self._entities[key] = entity
    
    def get(self, entity_class, entity_id):
        key = (entity_class, entity_id)
        return self._entities.get(key)
    
    def has(self, entity: BaseEntity):
        key = (entity.__class__, entity.id)
        return key in self._entities
    
    def remove(self, entity: BaseEntity):
        key = (entity.__class__, entity.id)
        self._entities.pop(key, None)
        
    def clear(self):
        self._entities.clear()
