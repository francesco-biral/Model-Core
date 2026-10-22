# Model-Core

A minimal, language-neutral manifest specification for reusable mathematical models.

**Status:** v0.1 prototype. The Maple and Mathematica exporters, code generation, model IR and C/C++ runtime are **planned, not implemented**. Example manifests describe interfaces, not executable physical models.

## Scope

- Explicit ODE, implicit DAE, algebraic and discrete model descriptions
- Named and ordered variables, parameters, functions, derivatives and conventions
- JSON Schema validation and basic semantic checks
- Three representative example manifests

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
modelcore validate examples/bicycle/model.yaml
modelcore inspect examples/multibody/model.yaml
pytest -q
```

## Design decisions

- The symbolic source (Maple/Mathematica) is authoritative for equations.
- `model.yaml` is the public interface contract, not a CAS expression dump.
- Arrays of variables have stable ordering for generated numerical interfaces.
- Parameter values and experimental identification provenance will be stored separately from model definitions.
- Generated artifacts will be reproducible and tested against CAS reference values in later milestones.

## Planned milestones

1. **v0.1:** Manifest schema, validator, CLI, representative examples.
2. **v0.2:** CAS-neutral JSON IR and Maple exporter.
3. **v0.3:** Mathematica exporter and numeric reference cases.
4. **v0.4:** C ABI, code generation and cross-backend consistency tests.

See `docs/index.qmd` for the design overview.
