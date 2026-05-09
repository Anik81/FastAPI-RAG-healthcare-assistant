import io


def test_generate_returns_answer(client, api_key):
    client.post(
        "/ingest",
        files={"file": ("gen_test.txt",
               io.BytesIO(b"Metformin is first-line for type 2 diabetes."),
               "text/plain")},
        headers={"X-API-Key": api_key},
    )
    resp = client.post(
        "/generate",
        json={"query": "What is the first line treatment for diabetes?"},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert len(data["sources"]) >= 1
    assert data["query_language"] == "en"


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
