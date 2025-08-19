from .providors import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers import BaseController


class VectorDBProvidorFactory:
    """
    Factory class to create instances of vector database providers.
    Currently supports QdrantDB.
    """
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    
    def create(self, provider: str):

        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                dp_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        return None
    
