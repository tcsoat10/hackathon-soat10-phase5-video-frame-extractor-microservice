from ast import alias
from mongoengine import connect, disconnect
import os

DELETE_MODE = os.getenv('DELETE_MODE', 'soft').lower()  # Default to 'soft' delete mode

class MongoDBConfig:
    """MongoDB configuration class"""
    
    @staticmethod
    def get_connection_string() -> str:
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        mongo_port = int(os.getenv('MONGO_PORT', 27017))
        mongodb_name = os.getenv('MONGO_DB', 'video_frame_extractor_microservice')
        mongo_user = os.getenv('MONGO_USER', '')
        mongo_password = os.getenv('MONGO_PASSWORD', '')
        auth_source = os.getenv('AUTH_SOURCE', 'admin')

        if mongo_user and mongo_password:
            connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongodb_name}?authSource={auth_source}"
        else:
            connection_string = f"mongodb://{mongo_host}:{mongo_port}"

        return connection_string
    
    @staticmethod
    def connect_to_database(alias='default'):

        """Connect to MongoDB"""
        try:
            # Disconnect existing connection if any
            try:
                disconnect(alias=alias)
            except:
                pass
            
            
            print("Connecting to MongoDB database...")
            print(f"Using alias: {alias}")
            # print(f"Connection string: {MongoDBConfig.get_connection_string()}")

            
            connection_string = MongoDBConfig.get_connection_string()
            mongo_db = os.getenv('MONGO_DB', 'video_frame_extractor_microservice')
            
            connect(
                db=mongo_db,
                host=connection_string,
                alias=alias,
                authentication_source='video_frame_extractor_microservice'
            )
            print(f"Connected to MongoDB: {mongo_db} with alias: {alias}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    @staticmethod
    def disconnect_from_database(alias='default'):
        """Disconnect from MongoDB"""
        try:
            disconnect(alias=alias)
            print(f"Disconnected from MongoDB (alias: {alias})")
        except Exception as e:
            print(f"Error disconnecting from MongoDB: {e}")

def connect_db(alias='default'):
    """Connect to MongoDB database"""
    
    print("Connecting to MongoDB database...")
    print(f"Using alias: {alias}")
    # print(f"Connection string: {MongoDBConfig.get_connection_string()}")
    
    MongoDBConfig.connect_to_database(alias=alias)


def disconnect_db(alias='default'):
    """Disconnect from MongoDB database"""
    MongoDBConfig.disconnect_from_database(alias=alias)


def get_db():
    """
    Get MongoDB connection for MongoEngine models
    """
    from mongoengine import get_db as mongoengine_get_db

    return mongoengine_get_db()

__all__ = ['MongoDBConfig', 'connect_db', 'disconnect_db', 'get_db']
