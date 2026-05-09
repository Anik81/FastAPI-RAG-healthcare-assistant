def test_missing_api_key(client):
    resp = client.post("/retrieve", json={"query": "test"})
    assert resp.status_code == 401


def test_wrong_api_key(client):
    resp = client.post(
        "/retrieve",
        json={"query": "test"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp.status_code == 401
