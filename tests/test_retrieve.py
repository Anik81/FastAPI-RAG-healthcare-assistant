import io


def _upload(client, api_key, filename, text):
    client.post(
        "/ingest",
        files={"file": (filename, io.BytesIO(text.encode("utf-8")), "text/plain")},
        headers={"X-API-Key": api_key},
    )


def test_retrieve_returns_results(client, api_key):
    _upload(client, api_key, "bp.txt",
            "Blood pressure management and hypertension treatment guidelines.")
    _upload(client, api_key, "asthma.txt",
            "Asthma treatment with inhaled corticosteroids.")
    _upload(client, api_key, "diabetes2.txt",
            "Diabetes care and insulin therapy.")

    resp = client.post(
        "/retrieve",
        json={"query": "How to manage blood pressure?"},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) >= 1
    assert data["query_language"] == "en"


def test_retrieve_empty_query_rejected(client, api_key):
    resp = client.post(
        "/retrieve",
        json={"query": ""},
        headers={"X-API-Key": api_key},
    )
    assert resp.status_code == 422
