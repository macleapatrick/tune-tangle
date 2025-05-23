from pymongo import MongoClient
import torch
from torch import Tensor
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel, BitsAndBytesConfig
import re
import html
from tqdm import tqdm

def main():
    # MongoDB connection
    client = MongoClient("mongodb://localhost:27017")
    source_db = client["tune_tangle"]
    source_coll = source_db["lyrics_db"]
    target_db = client["tune_tangle"]
    target_coll = target_db["lyrics_db"]

    # 1) Define your 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",  # you can also try "fp4" or "int4"
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )

    model = AutoModel.from_pretrained(
        "nvidia/nv-embed-v2",
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map = "auto"
    )
    model.eval()

    BATCH_SIZE = 500  # Tune this to your memory/throughput constraints
    query_base = {
        "language_cld3": "en",
        "views": {"$gt": 10000},
        "prompted_embedding": {"$exists": False}
    }
    projection = {
        "_id": 1,
        "lyrics": 1,
        "year": 1,
        "artist": 1,
        "tag": 1,
        "views": 1
    }

    while True:
        query = query_base.copy()

        batch = list(source_coll.find(query, projection).limit(BATCH_SIZE))
        if not batch:
            break

        for doc in batch:
            try:
                year, artist, tag, views = doc["year"], doc["artist"], doc["tag"], doc["views"]
                lyrics = clean_lyrics(doc["lyrics"])
                ids = doc["_id"]

                lyrics_instruction = (
                    f"Instruct: Embed the meaning of this song for retrieval and comparison.\n"
                    f"Metadata: Artist = {artist}, Genre = {tag}, Year = {year}, Popularity = {views}\n"
                )

                if len(lyrics) < 10000:
                    print(f"Processing lyrics... {str(ids)}")
                    process_batch(lyrics, ids, model, target_coll, instruction=lyrics_instruction)
                else:
                    print(f"Lyrics to long... {str(ids)}")
                    target_coll.update_one(
                        {"_id": ids},
                        {"$set": {"prompted_embedding": None}},
                        upsert=True
                    )


            except Exception as e:
                print(f"Error processing doc {doc.get('_id')}: {e}")


def process_batch(lyrics_batch, ids, model, target_coll, instruction):
    """
    Generate embeddings with NV-Embed-v2's high-level encode API and upsert into MongoDB.
    """
    # 1) Encode lyrics (handles tokenization, RoPE, batching)
    with torch.inference_mode():
        embeddings = model.encode(
            [lyrics_batch],
            instruction=instruction,
            max_length=32768,
        )

    # 2) Normalize embeddings (optional but often recommended)
    #embeddings = F.normalize(embeddings, p=2, dim=1)

    # 3) Persist to MongoDB
    target_coll.update_one(
        {"_id": ids},
        {"$set": {"prompted_embedding": embeddings.detach().cpu().tolist()}},
        upsert=True
    )

    torch.cuda.empty_cache()


def clean_lyrics(text: str) -> str:
    # 1) un-escape HTML entities
    text = html.unescape(text)

    # 2) remove any [BRACKETED SECTIONS] (Intro, Chorus, etc.)
    text = re.sub(r"\[.*?\]", " ", text)

    # 4) replace newlines and tabs with a single space
    text = re.sub(r"[\r\n\t]+", " ", text)

    # 5) remove any stray backslashes or escape-chars
    text = text.replace("\\", " ")

    # 6) collapse multiple spaces into one
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


if __name__ == "__main__":
    main()