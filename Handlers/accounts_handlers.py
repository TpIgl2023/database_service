from fastapi import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import Services.accounts_services as accounts_services
from Core.Enums.accounts_types import AccountType


async def create_account_handler(request: Request, db: Session):
    try:
        body = await request.json()

        assert body is not None, "Invalid body"
        assert "account_type" in request.headers, "Invalid account type"

        account_type = AccountType(request.headers["account_type"])

        if account_type == AccountType.USER or account_type == AccountType.MODERATOR:
            account = accounts_services.create_account(body, account_type, db)
        elif account_type == AccountType.ADMINISTRATOR:
            account = accounts_services.create_administrator(body, db)
        else:
            raise Exception("Invalid account type")

        return JSONResponse(status_code=200,
                            content={
                                "message": "Account created successfully",
                                "account": account,
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
        account_id = int(request.headers["id"])
        account_type = AccountType(request.headers["account_type"])

        if account_type != AccountType.ADMINISTRATOR:
            accounts_services.delete_account(account_id, db)
        else:
            accounts_services.delete_account(account_id, db)

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
        modified_account = accounts_services.update_account(body, db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Account updated successfully",
                                "modified_account": modified_account.to_dict()
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while updating account",
                                "error": str(e)
                            })


def get_account_by_id_handler(account_id: int, db: Session):
    try:
        account = accounts_services.get_account_by_id(account_id, db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Account retrieved successfully",
                                "account": account.to_dict()
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving account",
                                "error": str(e)
                            })


def get_moderators(db: Session):
    try:
        moderators = accounts_services.get_moderators(db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Moderators retrieved successfully",
                                "moderators": moderators
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving moderators",
                                "error": str(e)
                            })


def check_email_existence_handler(request: Request, db: Session):
    try:

        email = request.headers.get("email")

        is_exist = accounts_services.check_email_existence(email, db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Email checked successfully",
                                "is_exist": is_exist
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while checking email",
                                "error": str(e)
                            })


async def get_accounts_handler(request: Request, db: Session):
    try:

        body = await request.json()

        accounts = accounts_services.get_accounts(body, db)
        return JSONResponse(status_code=200,
                            content={
                                "message": "Accounts retrieved successfully",
                                "accounts": accounts
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving accounts",
                                "error": str(e)
                            })

