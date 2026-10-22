# Model-Core — Agent Development Instructions

## Mission
Build a reusable, language-neutral framework for symbolic mathematical models authored in Maple and Mathematica and exported for simulation, identification, optimal control, MPC, and real-time applications.

## Read before editing
1. `README.md`
2. `docs/architecture.qmd`
3. `docs/development-roadmap.qmd`
4. `docs/modelcore-guide.qmd`
5. Relevant source files and tests.

## Non-negotiable design decisions
- All code, comments, documentation, commit messages, and user-facing technical examples must be in English.
- Maple's primary source convention uses time-dependent functions: `xvars=[x(t),v(t)]`, `uvars=[F(t)]`, `pvars=[m,k,c]`, `usr_funcs=[...]`, and `ode_eqns=[...]`.
- Preserve the ordering of states, inputs, parameters, and outputs in every exported numerical interface.
- Support first-order explicit and implicit ODEs. Normalize equations to residuals without automatically solving for derivatives, expanding large expressions, or altering the authoritative symbolic source.
- User functions have ordered, potentially vector-valued signatures and optional symbolic bodies. Generate standalone implementations by default when a symbolic body exists; otherwise record an external dependency. Support hybrid symbolic/external implementations.
- For optimization, expose sparse Jacobian contracts and weighted Hessians of vector functions. External derivatives require explicit implementations or an explicitly selected compatible AD backend; never silently substitute finite differences.
- Treat models with thousands of nonlinear equations as a core use case: prefer streaming/chunked IR, deterministic ordering, bounded memory, and sparse operations. Do not indiscriminately expand or simplify the entire system.
- Separate mathematical model definitions, parameter sets, generated code, runtime interfaces, and application-specific OCP objectives/constraints.
- Maple/Mathematica remain authoritative for symbolic expressions. The Python tooling validates, packages, and transports metadata; it must not pretend to be a second CAS.
- Keep the compiled runtime independent of Maple, Mathematica, and Python.

## Current repository reality
- `src/modelcore/` contains Python schema validation/CLI, JSONL chunk transport, and derivative *capability declarations*.
- `maple/ModelCore.mpl` is an unverified prototype. Do not claim Maple execution or correctness without running Maple.
- Mathematica exporter, standalone C/C++ code generation, sparse symbolic differentiation, compilation, and production runtime are not implemented.
- The package metadata may still show version `0.1.0`; the term 'v0.2 prototype' describes the development milestone, not a verified release.
- Check actual files and tests before claiming functionality or test counts.

## Development workflow
1. Inspect the current implementation and relevant tests before making changes.
2. Make incremental, narrowly scoped changes; preserve backward compatibility unless a migration is documented.
3. Add/update tests for every implemented feature, including invalid inputs and edge cases.
4. Update `docs/architecture.qmd` for architecture changes, `docs/development-roadmap.qmd` for status, and the developer guide for public usage/API changes.
5. Mark pseudocode or unverified CAS snippets as **proposed** or **untested**.
6. Run `python -m pytest -q` after installing the package with `python -m pip install -e '.[dev]'`. If Maple or Mathematica is unavailable, report that limitation explicitly.
7. Report files changed, test results, outstanding risks, and follow-up tasks.
8. Do not commit, push, tag, or publish without explicit user authorization.

## Repository conventions
- `src/modelcore/`: reusable Python package implementation.
- `maple/`, `mathematica/`: CAS-specific sources and examples.
- `schema/`: public manifest schemas.
- `examples/`: reproducible model examples.
- `tests/`: automated checks.
- `docs/`: Quarto living documentation.
- `build/`, generated artifacts, caches, and local virtual environments are derived; do not commit them by default.
- Prefer explicit typed interfaces, portable paths, and stable machine-readable schema versions.

## Initial next milestone
Implement and verify the Maple `Model` object and `UserFunction` declarations (including vector signatures and symbolic/external/hybrid modes), residual normalization, robust validation, and reliable IR export. Keep code generation and derivative generation as separate subsequent milestones unless explicitly requested.
