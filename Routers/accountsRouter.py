from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

import Handlers.accountsHandlers as accountsHandler
from database import get_db

accountsRouter = APIRouter()


@accountsRouter.post("/create")
async def create_account(request: Request, db: Session = Depends(get_db)):
    return await accountsHandler.create_account_handler(request, db)


@accountsRouter.get("/")
async def create_account(request: Request):
    body = await request.json()
    return {"message": "Hello accounts router", "body": body}

