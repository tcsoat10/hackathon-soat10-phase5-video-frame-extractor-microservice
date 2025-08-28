from dependency_injector import containers, providers

from src.config.database import get_db
from src.core.shared.identity_map import IdentityMap


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)
