from fastapi import HTTPException

from env import API_KEY


def authenticate_api_key(key: str):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
