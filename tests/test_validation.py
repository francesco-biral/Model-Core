from pathlib import Path
from modelcore.validation import load_model, validate_model

ROOT = Path(__file__).resolve().parents[1]


def test_examples_valid():
    for name in ("bicycle", "tyre", "multibody"):
        path = ROOT / "examples" / name / "model.yaml"
        assert validate_model(load_model(path)) == []


def test_duplicate_name_rejected():
    model = load_model(ROOT / "examples/bicycle/model.yaml")
    model["parameters"].append({"name": "vx", "unit": "m/s"})
    assert any("Duplicate" in error for error in validate_model(model))


def test_unknown_derivative_function_rejected():
    model = load_model(ROOT / "examples/bicycle/model.yaml")
    model["derivatives"][0]["function"] = "unknown"
    assert any("unknown function" in error for error in validate_model(model))
