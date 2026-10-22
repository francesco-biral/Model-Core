# ModelCore v0.2 architecture decision record

## Model definition

The authoritative source is a Maple or Mathematica model, using ordered lists
`xvars`, `uvars`, `pvars`, `usr_funcs`, and `ode_eqns`. States and inputs are
functions of time. Explicit and implicit first-order ODEs are normalized to
residual equations without attempting to solve for derivatives.

## User functions

Declared user functions are **standalone by default**. A signature supports
scalar or vector inputs and outputs, with explicitly specified dimensions,
argument ordering, numerical types, and units. A function can have a symbolic
body, an external implementation, or both. Symbolic definitions may be used to
produce a standalone implementation. External functions require explicitly
registered derivatives when analytic NLP derivatives are requested.

## Derivatives for OCP/NLP

The preferred interface is the sparse Jacobian and the **weighted Hessian**
`H = d2(lambda^T F)/dw2`, rather than a separate dense Hessian for every
output component. For compositions, apply the chain rule using sparse block
structures and Jacobian-vector / vector-Jacobian products where useful.
The first implementation will use COO sparse triplets with a documented,
zero-based, deterministic ordering. A production backend may convert to CSR.

Do not silently substitute finite differences for missing derivatives. For
external functions, support registered first derivatives and weighted second
derivatives. Later versions may support AD-compatible C++ functions and
Hessian-vector products, but only where the toolchain supports them.

## Large model storage

Keep native CAS expressions in source files; avoid huge YAML manifests and
expanded expression strings in a single JSON file. The transport IR uses
chunked JSON Lines, with SHA-256 per chunk and streaming validation. For very
large models, generate numeric C/C++ in separate translation units and keep
symbolic common subexpressions and sparse derivative blocks intact.

**Important:** JSONL chunks in v0.2 are a transport format, not a portable
symbolic AST. CAS-independent expression semantics and code generation remain
future work. CSE should be scoped to manageable blocks, not applied globally
without memory limits. Store equation provenance and stable equation IDs.

## Status and limitations

Python IR chunking and derivative contracts are implemented and tested.
The Maple package is an initial, unexecuted prototype: CAS export,
user-function registry, sparse symbolic differentiation, standalone code
generation, and the Mathematica frontend are not yet implemented.
