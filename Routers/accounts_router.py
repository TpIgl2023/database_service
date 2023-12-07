from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

import Handlers.accounts_handlers as accounts_handler
from Database.database import get_db
from Models.account_model import Account

accountsRouter = APIRouter()


@accountsRouter.post("/create")
async def create_account(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.create_account_handler(request, db)


@accountsRouter.delete("/delete")
async def delete_account(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.delete_account_handler(request, db)


@accountsRouter.put("/update")
async def update_account(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.update_account_handler(request, db)


@accountsRouter.get("/moderators")
async def get_moderators(db: Session = Depends(get_db)):

    return accounts_handler.get_moderators(db)


@accountsRouter.get("/checkEmailExistence")
async def check_email_existence(request: Request, db: Session = Depends(get_db)):
    return accounts_handler.check_email_existence_handler(request, db)


@accountsRouter.get("/getAccounts")
async def get_accounts(request: Request, db: Session = Depends(get_db)):
    return await accounts_handler.get_accounts_handler(request, db)


@accountsRouter.get("/{account_id}")
async def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    return accounts_handler.get_account_by_id_handler(account_id, db)



