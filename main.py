from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from Routers.accountsRouter import accountsRouter
from Models.AccountModel import Account
from database import get_db

app = FastAPI()


app.include_router(accountsRouter, prefix="/accounts", tags=["accounts"])


@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    print(type(db))
    account = Account(name=body["name"], email=body["email"], password=body["password"], phone=body["phone"])
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

