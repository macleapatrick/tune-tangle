from pydantic import BaseModel, Field
from typing import Any, Dict, List

# ── Request models ──────────────────────────────────────────────
class VectorSearchByTextIn(BaseModel):
    query: str = Field(..., example="Hello darkness my old friend")
    limit: int = Field(5, ge=1, le=50)

class VectorSearchByIdIn(BaseModel):
    id: str = Field(..., example="42e1f146-xxxx-xxxx-xxxx-bc800d39f8a7")
    limit: int = Field(5, ge=1, le=50)

class SmartSearchIn(BaseModel):
    query: str = Field(..., example="Queen Bohemian Rhapsody")
    limit: int = Field(10, gt=0, le=50)

# ── Response model (shared) ────────────────────────────────────
class SearchHit(BaseModel):
    id: str
    score: float
    payload: Dict[str, Any]