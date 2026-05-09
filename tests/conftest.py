import os
import tempfile
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def api_key():
    return "test-key"


@pytest.fixture(scope="session", autouse=True)
def env(api_key):
    os.environ["SECRET_KEY"] = api_key
    os.environ["vector_store"] = tempfile.mkdtemp()
    yield


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)
