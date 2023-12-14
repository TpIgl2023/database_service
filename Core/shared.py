import json


def check_field_existence(json: dict, field: str):
    return field in json.keys() and json[field] is not None


async def get_request_body(request):
    body_bytes = await request.body()

    body_str = body_bytes.decode("utf-8")
    if not body_str:
        return {}
    body = json.loads(body_str)

    return body


