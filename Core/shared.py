
from Database.database import Base


def _check_field_existence(json: dict, field: str):
    return field in json.keys() and json[field] is not None


def _check_and_modify_field(original: [Base], modified: dict, field: str):
    if _check_field_existence(modified, field):
        original.name = modified[field]
