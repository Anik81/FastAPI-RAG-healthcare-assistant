# Healthcare Knowledge Assistant

A small RAG backend for clinicians. You can upload medical guideline `.txt` files in English or Japanese, search them with a query in either language, and get a short answer back. The answer can be returned in English or Japanese.

## Tech stack

- FastAPI for the API
- FAISS (`IndexFlatIP`) for vector search
- sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2` for embeddings (works for both English and Japanese)
- Helsinki-NLP MarianMT for the optional translation
- langdetect for picking up the query language
- pytest + ruff for tests and linting
- Docker + GitHub Actions for the build and image push

## Project structure

```
app/
├── main.py
├── auth.py
├── settings.py
├── models.py
├── routers/
│   ├── ingest.py
│   ├── retrieve.py
│   └── generate.py
└── services/
    ├── create_embeddings.py
    ├── language_detection.py
    ├── vector_store.py
    └── rag.py
docs/                          (sample EN/JA documents)
tests/
.github/workflows/ci.yml
Dockerfile
```

## Setup

### Run the published Docker image

```bash
docker pull ghcr.io/anik81/fastapi-rag-healthcare-assistant:latest
docker run -p 8000:8000 -e SECRET_KEY="testkey" \
  ghcr.io/anik81/fastapi-rag-healthcare-assistant:latest
```

Then open http://localhost:8000/docs.

### Build the image yourself

```bash
git clone https://github.com/Anik81/FastAPI-RAG-healthcare-assistant.git
cd FastAPI-RAG-healthcare-assistant
docker build -t healthcare-rag .
docker run -p 8000:8000 -e SECRET_KEY="testkey" healthcare-rag
```

First build takes 5 to 10 minutes because it pre downloads the embedding model (about 470 MB) into the image.

### Run from source

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API examples

All endpoints except `/health` need the `X-API-Key` header. Examples below use `testkey`.

### Health check

```bash
curl http://localhost:8000/health
```

```json
{"status": "ok"}
```

### Ingest a document

```bash
curl -X POST http://localhost:8000/ingest \
  -H "X-API-Key: testkey" \
  -F "file=@docs/diabetes_en.txt"
```

```json
{
  "id": "0",
  "language": "en",
  "num_chunks": 1,
  "source": "diabetes_en.txt"
}
```

### Retrieve top results

```bash
curl -X POST http://localhost:8000/retrieve \
  -H "X-API-Key: testkey" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the first line treatment for type 2 diabetes?", "top_k": 3}'
```

```json
{
  "query_language": "en",
  "results": [
    {
      "id": "0",
      "text": "Type 2 diabetes management focuses on lifestyle modification...",
      "score": 0.71,
      "language": "en",
      "source": "diabetes_en.txt"
    },
    {
      "id": "1",
      "text": "2型糖尿病の管理では、食事療法、定期的な運動...",
      "score": 0.58,
      "language": "ja",
      "source": "diabetes_ja.txt"
    }
  ]
}
```

The English query also matched the Japanese document. That happens because the embedding model puts both languages into the same vector space.

### Generate an answer

```bash
curl -X POST http://localhost:8000/generate \
  -H "X-API-Key: testkey" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the first line treatment for type 2 diabetes?"}'
```

```json
{
  "query_language": "en",
  "output_language": "en",
  "answer": "Based on 3 retrieved document(s) (diabetes_en.txt, diabetes_ja.txt, hypertension_en.txt), the most relevant information is: Type 2 diabetes management focuses on lifestyle modification...",
  "sources": [
    {"id": "0", "source": "diabetes_en.txt", "score": 0.71},
    {"id": "1", "source": "diabetes_ja.txt", "score": 0.58}
  ]
}
```

To get the answer in the other language, add `output_language`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "X-API-Key: testkey" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the first line treatment for type 2 diabetes?", "output_language": "ja"}'
```

The `answer` field comes back translated.

## Tests

```bash
pytest -q
```
