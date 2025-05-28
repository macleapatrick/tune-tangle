from rapidfuzz import fuzz
from typing import List, Dict
from qdrant_client import models as qm
from .schemas import (
    SearchHit,
)

from .core import COLLECTION

def smart_search(
    query_str: str,
    client,
    limit: int = 20,
    overfetch: int = 100,
) -> List[SearchHit]:
    """
    Text-only search that matches query_str against `title`, `artist` Results are ordered by a RapidFuzz
    token-set ratio (0-1).  `limit` = how many hits to return.
    """

    # 1) OR-filter over the three fields
    qfilter = qm.Filter(
        should=[
            qm.FieldCondition(key="title",  match=qm.MatchText(text=query_str)),
            qm.FieldCondition(key="artist", match=qm.MatchText(text=query_str)),
        ]
    )

    # 2) Grab a slice of matching points (no vector → use SCROLL)
    points, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=qfilter,
        with_payload=True,
        limit=overfetch,
    )

    # 3) Local fuzzy ranking
    scored = []
    q_low  = query_str.lower()
    for p in points:
        meta = p.payload
        corpus_text = " ".join(
            str(meta.get(k, "")) for k in ("artist", "title")
        ).lower()
        fuzzy = fuzz.token_set_ratio(q_low, corpus_text) / 100.0  # 0-1
        scored.append(
            {
                "id":       str(p.id),
                "payload":  meta,
                "score":    round(fuzzy, 3),
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    scored = scored[:limit]
    return [SearchHit(id=str(s.get("id")), score=s.get("score"), payload=s.get("payload")) for s in scored]