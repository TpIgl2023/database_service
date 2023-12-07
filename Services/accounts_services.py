from sqlalchemy.orm import Session

from Core.Enums.accounts_types import AccountType
from Models.account_model import Account
from Models.admin_model import Administrator
from Models.moderator_model import Moderator
from Models.user_model import User

'''
    Account creation functions
'''


def create_account(account_json: dict, account_type: AccountType, db: Session):
    with db.begin():

        account = _create_account(account_json, db)

        if account_type == AccountType.USER:
            _create_user(account.id, db)
        elif account_type == AccountType.MODERATOR:
            _create_moderator(account.id, db)

        db.commit()
        db.flush()

    return account

'''
def create_user(account_json: dict, db: Session ):

    with db.begin():

        account = _create_account(account_json, db)

        _create_user(account.id, db)

        db.commit()
        db.flush()

    return account


def create_moderator(account_json: dict, db: Session):
    with db.begin():

        account = _create_account(account_json, db)

        _create_moderator(account.id, db)

        db.commit()
        db.flush()

    return account

'''
def create_administrator(account_json: dict, db: Session):
    with db.begin():

        account = _create_account(account_json, db)

        _create_administrator(account.id, db)

        db.commit()
        db.flush()

    return account


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


def _create_administrator(_id: int, db: Session):

    admin = Administrator(id=_id)
    db.add(admin)
    return admin


'''
    Account deletion functions
'''


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



'''
    Account modification functions 
'''


def update_account(modified_account_json: dict, db: Session):
    assert modified_account_json is not None, "Invalid account json"
    assert modified_account_json["id"] is not None, "Invalid account id"

    original_account = db.query(Account).filter_by(id=modified_account_json["id"]).first()

    assert original_account, "Account not found"

    fields = ["name", "email", "password", "phone"]

    for field in fields:
        _check_and_midify_field(original_account, modified_account_json, field)

    db.commit()

    return original_account


def _check_field_existence(json: dict, field: str):
    return field in json.keys() and json[field] is not None


def _check_and_midify_field(original: Account, modified: dict, field: str):
    if _check_field_existence(modified, field):
        original.name = modified[field]


def get_account_by_id(account_id: int, db: Session):
    return db.query(Account).filter(Account.id == account_id).first()


def get_moderators(db: Session):

    mods = db.query(Moderator).all()

    mods_json = []
    for mod in mods:
        mods_json.append(mod.account.to_dict())
    return mods_json




