from .providors import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers import BaseController


class VectorDBProviderFactory:
    """
    Factory class to create instances of vector database providers.
    Currently supports QdrantDB.
    """
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    @staticmethod
    def create(self, provider: str, **kwargs):
        """
        Create a vector database provider instance based on the provider name.
        
        :param provider_name: Name of the vector database provider (e.g., 'QdrantDB').
        :param kwargs: Additional parameters for provider initialization.
        :return: An instance of the specified vector database provider.
        """
        
        if provider == VectorDBEnums.QDRANT.value:
            return QdrantDBProvider(
                dp_path=self.config.VECTOR_DB_PATH,
                distance_method=None
            )
        
        return None
    
