import json


def validate_json(data: str) -> tuple:
    try:
        json_data = json.loads(data)
        return json_data, True
    except Exception:
        return None, False
