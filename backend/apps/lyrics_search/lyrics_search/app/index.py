from qdrant_client import models as qm

from .core import get_qdrant, COLLECTION

def index():
    client = get_qdrant()
    # One-time: full-text indexes on the two fields
    for field in ("title", "artist"):
        client.create_payload_index(
            collection_name=COLLECTION,
            field_name=field,
            field_schema=qm.TextIndexParams(
                type="text",
                tokenizer=qm.TokenizerType.PREFIX,
                min_token_len=2,
                lowercase=True,
            ),
        )

if __name__ == "__main__":
    index()