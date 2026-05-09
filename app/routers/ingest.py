from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth import verify_secret_key
from app.services import create_embeddings, vector_store
from app.services.language_detection import detect_language
from app.models import IngestResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse,
             dependencies=[Depends(verify_secret_key)])
 
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(400, "Only .txt files accepted")
    raw = await file.read()
    text = raw.decode("utf-8").strip()
    if not text:
        raise HTTPException(400, "Empty file")

    lang = detect_language(text)
    vec = create_embeddings.vectorize(text)
    s = vector_store.get_store()
    new_id = s.insert(vec, text=text, language=lang, source=file.filename)

    return IngestResponse(
        id=new_id, language=lang, num_chunks=1, source=file.filename
    )