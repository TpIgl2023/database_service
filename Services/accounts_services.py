from fastapi import Depends
from sqlalchemy.orm import Session

from Core.Enums.accounts_types import AccountType
from Models.account_model import Account
from Models.moderator_model import Moderator
from Models.user_model import User


def create_account(account_json: dict, account_type: AccountType, db: Session):

    assert (account_type is not None) and (account_type in AccountType), "Invalid account type"
    assert account_json is not None, "Invalid account json"
    with db.begin():

        account = _create_account(account_json, db)

        if account_type == AccountType.USER:

            _create_user(account.id, db)

        else:

            _create_moderator(account.id, db)

        db.commit()
        db.flush()

    return account, account_type


def _create_account(account_json: dict, db: Session):

    account = Account.from_dict(account_json)
    db.add(account)
    db.flush()

    return account


def _create_user(_id: int, db: Session):
    user = User(id=_id)
    db.add(user)
    return user


def _create_moderator(_id: int, db: Session):

    mod = Moderator(id=_id)
    db.add(mod)
    return mod


def delete_account(account_id: int, db: Session):

    assert account_id is not None, "Invalid account json"
    with db.begin():
        account = _delete_account(account_id, db)
        db.commit()
        db.flush()

    return account


def _delete_account(account_id: int, db: Session):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise Exception("Account not found")

    db.delete(account)

    return account


def _delete_user(account_id: int, db: Session):
    user = db.query(User).filter(User.id == account_id).first()
    if user is None:
        raise Exception("User not found")

    db.delete(user)

    return user


def _delete_moderator(account_id: int, db: Session):
    mod = db.query(Moderator).filter(Moderator.id == account_id).first()
    if mod is None:
        raise Exception("Moderator not found")

    db.delete(mod)

    return mod

