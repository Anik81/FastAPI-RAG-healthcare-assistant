from fastapi import APIRouter, Depends
from app.auth import verify_secret_key
from app.services import create_embeddings, vector_store
from app.services.language_detection import detect_language
from app.models import RetrieveRequest, RetrieveResponse

router = APIRouter()


@router.post("/retrieve", response_model=RetrieveResponse,
             dependencies=[Depends(verify_secret_key)])

def retrieve(payload: RetrieveRequest):
    embeddings = create_embeddings.vectorize(payload.query)
    matches = vector_store.get_store().search(embeddings, k=payload.top_k)
    return RetrieveResponse(
        query_language=detect_language(payload.query),
        results=matches,
    )
