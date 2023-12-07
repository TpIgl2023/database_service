
from Database.database import Base


def check_field_existence(json: dict, field: str):
    return field in json.keys() and json[field] is not None


