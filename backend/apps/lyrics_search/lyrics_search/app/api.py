import torch.nn.functional as F
from fastapi import APIRouter, HTTPException
from .search import smart_search
from .core import Client, Model, COLLECTION
from .schemas import (
    VectorSearchByTextIn,
    VectorSearchByIdIn,
    SmartSearchIn,
    SearchHit,
)

router = APIRouter()
client = Client()
model = Model()

# -------- A) Embed-and-search ----------------------------------
@router.post("/search/vector/text", response_model=list[SearchHit])
def vector_search_by_text(body: VectorSearchByTextIn):
    instructions = "Find the song lyrics that most closely matches the following query:\n\n"
    query_vector = model.get_embedder.encode([body.query], instructions=instructions, max_length=32768)
    query_vector= F.normalize(query_vector, p=2, dim=1)

    hits = client.get_qdrant.search(
        collection_name=COLLECTION,
        query_vector=query_vector.detach().cpu().numpy().flatten().tolist(),
        limit=body.limit,
        with_payload=True,
    )

    return [SearchHit(id=str(h.id), score=h.score, payload=h.payload) for h in hits]

# -------- B) Re-use existing point vector ----------------------
@router.post("/search/vector/id", response_model=list[SearchHit])
def vector_search_by_id(body: VectorSearchByIdIn):

    # Grab the point to use its stored vector
    points = client.get_qdrant.retrieve(
        collection_name=COLLECTION,
        ids=[body.id],
        with_vectors=True,
        with_payload=False,
    )
    if not points or points[0].vector is None:
        raise HTTPException(404, f"Point id '{body.id}' not found or has no vector.")

    query_vector = points[0].vector

    hits = client.get_qdrant.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=body.limit,
        with_payload=True,
    )
    return [SearchHit(id=str(h.id), score=h.score, payload=h.payload) for h in hits]


# -------- (unchanged) payload-only search ----------------------
@router.post("/search/smart", response_model=list[SearchHit])
def payload_search(body: SmartSearchIn):
    return smart_search(body.query, client.get_qdrant, limit=body.limit)