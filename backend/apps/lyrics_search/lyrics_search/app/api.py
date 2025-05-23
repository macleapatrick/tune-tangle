from fastapi import APIRouter, HTTPException
from .search import smart_search
from .core import get_qdrant, COLLECTION
from .schemas import (
    VectorSearchByTextIn,
    VectorSearchByIdIn,
    SmartSearchIn,
    SearchHit,
)

router = APIRouter()

# -------- A) Embed-and-search ----------------------------------
@router.post("/search/vector/text", response_model=list[SearchHit])
def vector_search_by_text(body: VectorSearchByTextIn):
    pass

# -------- B) Re-use existing point vector ----------------------
@router.post("/search/vector/id", response_model=list[SearchHit])
def vector_search_by_id(body: VectorSearchByIdIn):
    qdrant = get_qdrant()

    # Grab the point to use its stored vector
    points = qdrant.retrieve(
        collection_name=COLLECTION,
        ids=[body.id],
        with_vectors=True,
        with_payload=False,
    )
    if not points or points[0].vector is None:
        raise HTTPException(404, f"Point id '{body.id}' not found or has no vector.")

    query_vector = points[0].vector

    hits = qdrant.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=body.limit,
        with_payload=True,
    )
    return [SearchHit(id=str(h.id), score=h.score, payload=h.payload) for h in hits]


# -------- (unchanged) payload-only search ----------------------
@router.post("/search/smart", response_model=list[SearchHit])
def payload_search(body: SmartSearchIn):
    return smart_search(body.query, limit=body.limit)