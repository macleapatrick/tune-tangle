from functools import cached_property
from qdrant_client import QdrantClient
from typing import Any

import torch
from transformers import AutoModel, BitsAndBytesConfig

QDRANT_HOST = "ec2-13-217-233-161.compute-1.amazonaws.com"
QDRANT_PORT = 6333
COLLECTION = "lyrics"

class Client:

    def __init__(self):
        pass

    @cached_property
    def get_qdrant(self) -> QdrantClient:
        """
        load and cache the Qdrant client
        """
        return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

class Model:

    def __init__(self):
        pass

    @cached_property
    def get_embedder(self) -> Any:
        """
        load and cache 4-bit quantized  nv-embed-v2 embedder
        """

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        model = AutoModel.from_pretrained(
            "nvidia/nv-embed-v2",
            trust_remote_code=True,
            quantization_config=bnb_config,
            device_map="auto"
        )

        model.eval()

        return model