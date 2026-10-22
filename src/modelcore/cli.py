"""ModelCore command-line interface."""
import argparse
import sys
from .validation import load_model, validate_model


def main():
    parser = argparse.ArgumentParser(prog="modelcore")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "inspect"):
        command = sub.add_parser(name)
        command.add_argument("manifest")
    args = parser.parse_args()
    try:
        model = load_model(args.manifest)
        errors = validate_model(model)
        if errors:
            for error in errors:
                print("ERROR:", error, file=sys.stderr)
            return 1
        if args.command == "inspect":
            print(f"{model['model']['id']} v{model['model']['version']}")
            print("Formulation:", model["formulation"]["type"])
            for group, items in model.get("variables", {}).items():
                print(f"{group}: {', '.join(v['name'] for v in items)}")
            print("Functions:", ", ".join(f["name"] for f in model["functions"]))
        else:
            print("VALID:", args.manifest)
        return 0
    except (OSError, ValueError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
