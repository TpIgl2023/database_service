from fastapi import HTTPException, Request

from Services.auth_services import authenticate_api_key


def authenticate_api_key_middleware(request: Request):
    try:
        authenticate_api_key(request.headers["x-api-key"])
    except KeyError as e:
        raise HTTPException(status_code=401, detail="API key not found")
