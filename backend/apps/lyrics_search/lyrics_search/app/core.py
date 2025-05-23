from functools import cached_property
from qdrant_client import QdrantClient

QDRANT_HOST = "ec2-13-217-233-161.compute-1.amazonaws.com"
QDRANT_PORT = 6333
COLLECTION = "lyrics"

def get_qdrant() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
