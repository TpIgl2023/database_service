from Models import account_model, admin_model, moderator_model,  user_model, article_model, favorite_model
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from datetime import date
from sqlalchemy import Date

from Middlwares.auth_middlewares import authenticate_api_key_middleware
from Routers.accounts_router import accountsRouter
from Routers.articles_router import articlesRouter
from Database.database import get_db

app = FastAPI()


@app.middleware("http")
async def authenticate_api_key(request: Request, call_next):
    try:
        authenticate_api_key_middleware(request)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    response = await call_next(request)
    return response

app.include_router(accountsRouter, prefix="/accounts", tags=["accounts"])
app.include_router(articlesRouter, prefix="/articles", tags=["articles"])


@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    return {"body": body, "message": "Hello World"}
