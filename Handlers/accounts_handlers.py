from flask import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import Services.accounts_services as accountsServices
from Core.Enums.accounts_types import AccountType


async def create_account_handler(request: Request, db: Session):
    try:
        body = await request.json()

        account_type = AccountType(request.headers["account_type"])

        account, account_type = accountsServices.create_account(body, account_type, db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Account created successfully",
                                "account": account.to_dict(),
                                "account_type": account_type.value
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating account",
                                "error": str(e)
                            })
