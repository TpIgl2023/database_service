from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

import Handlers.accounts_handlers as accounts_handler
from Database.database import get_db

accountsRouter = APIRouter()


@accountsRouter.post("/create")
async def create_account(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.create_account_handler(request, db)


@accountsRouter.delete("/delete")
async def delete_account(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.delete_account_handler(request, db)



