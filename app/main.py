from fastapi import FastAPI
from app.routers import ingest, retrieve, generate

app = FastAPI(title="Healthcare Knowledge Assistant")

app.include_router(ingest.router)
app.include_router(retrieve.router)
app.include_router(generate.router)


@app.get("/health")
def health():
    return {"status": "ok"}