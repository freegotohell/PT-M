import json


def load_json(path: str = "settings.json") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"file {path} not found")
    except Exception as e:
        raise RuntimeError(f"file reading error {path}: {e}")