import secrets
from fastapi import Header, HTTPException, status
from app.settings import SECRET_KEY

def verify_secret_key(x_api_key: str = Header(None)):
    if not x_api_key or not secrets.compare_digest(x_api_key, SECRET_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key")