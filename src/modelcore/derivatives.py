"""Derivative interface contracts for symbolic and external user functions.

The API declares derivative capabilities; it does not synthesize derivative
implementations or silently use finite differences.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DerivativeContract:
    function: str
    input_size: int
    output_size: int
    jacobian_symbol: str | None = None
    weighted_hessian_symbol: str | None = None
    sparse_format: str = "coo"

    def __post_init__(self):
        if self.input_size < 1 or self.output_size < 1:
            raise ValueError("Input and output sizes must be positive")
        if self.sparse_format not in ("coo", "csr", "dense"):
            raise ValueError("Unsupported sparse format")

    def require_for_nlp(self, second_order=True):
        missing = []
        if self.jacobian_symbol is None:
            missing.append("Jacobian")
        if second_order and self.weighted_hessian_symbol is None:
            missing.append("weighted Hessian")
        if missing:
            raise ValueError(f"{self.function}: missing {', '.join(missing)} implementation(s)")
        return True
