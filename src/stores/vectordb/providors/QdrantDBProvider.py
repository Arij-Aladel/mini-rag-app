from qdrant_client import QdrantClient, models
from ..VectorDBInterface import  VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
from models.db_schemes import RetrievedDocument


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, dp_path: str, distance_method: str):
        
        self.client = None
        self.dp_path = dp_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT_PRODUCT.value:
            self.distance_method = models.Distance.DOT_PRODUCT

        self.logger = logging.getLogger(__name__)



    def connect(self):
        # Implement connection logic here
        self.logger.info("Connecting to QdrantDB...")
        self.client = QdrantClient(path=self.dp_path, distance=self.distance_method)
        

    def disconnect(self):
        # Implement disconnection logic here
        self.logger.info("Disconnecting from QdrantDB...")
        self.client = None

    def is_connection_existed(self, collection_name: str) -> bool:
        # Check if a connection to the specified collection exists
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> List:
        # List all collections in the vector database
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
        # Get information about a specific collection
        return self.client.get_collection(collection_name=collection_name)

    def create_collection(self, collection_name: str, embedding_size: int, 
                          do_reset: bool = False) -> bool:
        # Create a new collection in the vector database
        if do_reset:
            _ = self.delete_collection(collection_name)
        
        if not self.is_connection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, 
                    distance=self.distance_method
                    )
            )

            return True
        
        return False

    def delete_collection(self, collection_name: str) -> bool:
        # Delete a collection from the vector database
        if self.is_connection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
        return False    

    def insert_one(self, collection_name: str, text: str, vector: list,
                   metadata: dict = None,
                   record_id: int = None):
        # Insert a single record into the specified collection
        
        if not self.is_connection_existed(collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
            collection_name=collection_name,    
            records=[models.Record(
                id=record_id,
                vector=vector,
                payload={
                    "text": text,
                    "metadata" : metadata
                }
                )
            ]
             )
        except Exception as e:
            self.logger.error(f"Error inserting batch: {e}")
            return False
        
        return True


    def insert_many(self, collection_name: str, texts: list,
                    vectors: list, metadata: list = None,
                    record_ids: list = None, batch_size: int = 50):
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]
            batch_metadata = metadata[i:i + batch_size]
            batch_record_ids = record_ids[i:i + batch_size] if record_ids else None

            records = [
                models.Record(
                    id=record_id,
                    vector=vector,
                    payload={
                        "text": text,
                        "metadata": meta
                    }
                )
                for record_id, text, vector, meta in zip(batch_record_ids, batch_texts, batch_vectors, batch_metadata)
            ]

            if not self.is_connection_existed(collection_name):
                self.logger.error(f"Can not insert new records to non-existed collection: {collection_name}")
                return False
            
            try:
                _ = self.client.upload_records(
                collection_name=collection_name,
                records=records
            )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False
            
        return True 
    
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None
        
        return [
            RetrievedDocument(**{
                "score": result.score,
                "text": result.payload["text"],
            })
            for result in results
        ]