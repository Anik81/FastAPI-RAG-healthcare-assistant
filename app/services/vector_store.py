import json
import faiss
from app.settings import vector_store, embedding_dimension

class FaissStore:
    def __init__(self):
        self.index_path = vector_store / "faiss.index"
        self.docs_path = vector_store / "docs.json"
        self.index = faiss.IndexFlatIP(embedding_dimension)
        self.docs = {}
        self._load()

    def _load(self):
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        if self.docs_path.exists():
            self.docs = json.loads(self.docs_path.read_text(encoding="utf-8"))

    def _save(self):
        faiss.write_index(self.index, str(self.index_path))
        self.docs_path.write_text(
            json.dumps(self.docs, ensure_ascii=False), encoding="utf-8"
        )

    def insert(self, vector, text, language, source):
        new_id = str(self.index.ntotal)
        self.index.add(vector)
        self.docs[new_id] = {
            "text": text, "language": language, "source": source
        }
        self._save()
        return new_id

    def search(self, vector, k=3):
        if self.index.ntotal == 0:
            return []
        scores, ids = self.index.search(vector, k)
        results = []
        for s, i in zip(scores[0], ids[0]):
            if i == -1:
                continue
            m = self.docs.get(str(i), {})
            results.append({
                "id": str(i),
                "text": m.get("text", ""),
                "score": round(float(s), 2),
                "language": m.get("language", "unknown"),
                "source": m.get("source", ""),
            })
        return results


_store = None


def get_store():
    global _store
    if _store is None:
        _store = FaissStore()
    return _store