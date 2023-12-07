from flask import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import Services.accounts_services as accountsServices
from Core.Enums.accounts_types import AccountType


async def create_account_handler(request: Request, db: Session):
    try:
        body = await request.json()

        assert body is not None, "Invalid body"
        assert "account_type" in request.headers, "Invalid account type"

        account_type = AccountType(request.headers["account_type"])

        if account_type == AccountType.USER:
            account = accountsServices.create_user(body, db)
        elif account_type == AccountType.MODERATOR:

            assert "admin_id" in request.headers, "Invalid admin id"
            admin_id = int(request.headers["admin_id"])
            account = accountsServices.create_moderator(body, admin_id, db)
        elif account_type == AccountType.ADMINISTRATOR:
            account = accountsServices.create_administrator(body, db)

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


async def delete_account_handler(request: Request, db: Session):
    try:
        account_id = request.headers["id"]

        accountsServices.delete_account(account_id,  db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Account deleted successfully",
                                "account_id": account_id,
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while deleting account",
                                "error": str(e)
                            })


async def update_account_handler(request: Request, db: Session):
    try:
        body = await request.json()
        modified_account = await accountsServices.update_account(body, db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Account updated successfully",
                                "body": modified_account
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while updating account",
                                "error": str(e)
                            })
