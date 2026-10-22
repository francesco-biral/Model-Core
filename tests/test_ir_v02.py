import json
import pytest
from modelcore.ir import write_equation_chunks, iter_equation_chunks
from modelcore.derivatives import DerivativeContract


def test_streaming_large_ir(tmp_path):
    items = ({"id": i, "residual": f"r{i}"} for i in range(1050))
    index = write_equation_chunks(items, tmp_path, chunk_size=128)
    assert index["equation_count"] == 1050
    assert len(index["chunks"]) == 9
    assert list(iter_equation_chunks(tmp_path))[-1]["id"] == 1049


def test_corrupt_chunk(tmp_path):
    write_equation_chunks([{"id": 0}], tmp_path)
    (tmp_path / "equations-000000.jsonl").write_text('{"id": 1}\n')
    with pytest.raises(ValueError, match="Corrupted"):
        list(iter_equation_chunks(tmp_path))


def test_external_derivatives_must_be_declared():
    f = DerivativeContract("TyreFy", input_size=3, output_size=2,
                           jacobian_symbol="TyreFy_J")
    with pytest.raises(ValueError, match="weighted Hessian"):
        f.require_for_nlp()
    assert f.require_for_nlp(second_order=False)
    g = DerivativeContract("TyreFy", 3, 2, "TyreFy_J", "TyreFy_WH")
    assert g.require_for_nlp()
