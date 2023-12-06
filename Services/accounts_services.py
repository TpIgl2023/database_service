from fastapi import Depends
from sqlalchemy.orm import Session

from Core.Enums.accounts_types import AccountType
from Models.account_model import Account
from Models.moderator_model import Moderator
from Models.user_model import User
from Database.database import get_db


def create_account(account_json: dict, account_type: AccountType, db: Session = Depends(get_db)):

    assert account_type in AccountType, "Invalid account type"
    assert account_json is not None, "Invalid account json"
    with db.begin():
        account = _create_account(account_json, db)

        if account_type == AccountType.USER.value:
            _create_user(account.id, db)
        elif account_type == AccountType.MODERATOR:
            _create_moderator(account.id, db)

    db.flush()

    return account, account_type


def _create_account(account_json: dict, db: Session):

    account = Account.from_dict(account_json)
    db.add(account)
    db.commit()

    return account


def _create_user(_id: int, db: Session):
    user = User(id=_id)
    db.add(user)
    db.commit()
    return user


def _create_moderator(_id: int, db: Session):

    with db.begin():
        mod = Moderator(id=_id)
        db.add(mod)
        db.commit()
        db.refresh(mod)
    return mod

