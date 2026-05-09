import io


def test_ingest_en(client, api_key):
    content = b"Type 2 diabetes management focuses on lifestyle changes."
    resp = client.post(
        "/ingest",
        files={"file": ("diabetes.txt", io.BytesIO(content), "text/plain")},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["language"] == "en"
    assert data["source"] == "diabetes.txt"
    assert data["num_chunks"] == 1


def test_ingest_ja(client, api_key):
    content = "2型糖尿病の管理では生活習慣の改善が重要です。".encode("utf-8")
    resp = client.post(
        "/ingest",
        files={"file": ("diabetes_ja.txt", io.BytesIO(content), "text/plain")},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 200
    assert resp.json()["language"] == "ja"


def test_ingest_rejects_non_txt(client, api_key):
    resp = client.post(
        "/ingest",
        files={"file": ("data.csv", io.BytesIO(b"a,b,c"), "text/plain")},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 400
