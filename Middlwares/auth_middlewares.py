from fastapi import HTTPException
from flask import Request

from Services.auth_services import authenticate_api_key


def authenticate_api_key_middleware(request: Request):
    try:
        authenticate_api_key(request.headers["X-API-KEY"])
    except KeyError as e:
        raise HTTPException(status_code=401, detail="API key not found")
