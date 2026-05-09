from sentence_transformers import SentenceTransformer
from app.settings import MODEL_NAME

cached_model = None


def load_model():
    global cached_model
    if cached_model is None:
        cached_model = SentenceTransformer(MODEL_NAME)
    return cached_model


def vectorize(texts):
    if isinstance(texts, str):
        texts = [texts]
    vectors = load_model().encode(texts, normalize_embeddings=True)
    return vectors.astype("float32")