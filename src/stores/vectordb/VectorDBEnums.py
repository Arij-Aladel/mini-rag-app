from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "qdrant"

class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT_PRODUCT = "dot_product"