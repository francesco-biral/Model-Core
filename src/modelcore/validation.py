"""Schema and semantic validation for ModelCore manifests."""
import json
from pathlib import Path
from importlib.resources import files

import yaml
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema" / "model.schema.json"


def load_model(path):
    path = Path(path)
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream) if path.suffix.lower() == ".json" else yaml.safe_load(stream)
    return data


def validate_model(data):
    with SCHEMA_PATH.open(encoding="utf-8") as stream:
        schema = json.load(stream)
    errors = [f"{'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in Draft202012Validator(schema).iter_errors(data)]
    variables = data.get("variables", {}) if isinstance(data, dict) else {}
    names = []
    if isinstance(variables, dict):
        for group in variables.values():
            if isinstance(group, list):
                names.extend(v.get("name") for v in group if isinstance(v, dict))
    names.extend(v.get("name") for v in data.get("parameters", []) if isinstance(v, dict))
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        errors.append("Duplicate variable/parameter names: " + ", ".join(duplicates))
    function_names = {f.get("name") for f in data.get("functions", []) if isinstance(f, dict)}
    for derivative in data.get("derivatives", []):
        if derivative.get("function") not in function_names:
            errors.append(f"Derivative refers to unknown function: {derivative.get('function')}")
    return errors
