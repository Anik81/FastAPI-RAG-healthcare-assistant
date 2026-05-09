import os
from pathlib import Path

SECRET_KEY = os.environ.get("SECRET_KEY", "TANVIR RAHMAN ANIK")
MODEL_NAME = os.environ.get(
    "MODEL_NAME",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)

vector_store = Path(os.environ.get("vector_store", "./vector_storage"))
vector_store.mkdir(exist_ok=True)
embedding_dimension = 384