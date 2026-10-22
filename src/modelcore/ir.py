"""Compact, streaming ModelCore IR v0.2 for large symbolic models.

Equations are stored as newline-delimited JSON in independently addressable
chunks. The manifest contains only metadata and checksums; it does not inline
thousands of expanded symbolic expressions.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path


def write_equation_chunks(equations, directory, chunk_size=256):
    """Write an iterable of equation records without materializing it as a list.

    Records must be JSON-compatible dictionaries. This transport preserves
    strings but does NOT define a portable symbolic expression grammar.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    manifest = {"ir_version": "0.2", "encoding": "jsonl-utf8", "chunks": [], "equation_count": 0}
    stream = None
    digest = None
    count = 0
    try:
        for record in equations:
            if count % chunk_size == 0:
                if stream is not None:
                    stream.close()
                    manifest["chunks"][-1]["sha256"] = digest.hexdigest()
                filename = f"equations-{count // chunk_size:06d}.jsonl"
                stream = (directory / filename).open("wb")
                digest = hashlib.sha256()
                manifest["chunks"].append({"path": filename, "count": 0})
            raw = (json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
            stream.write(raw)
            digest.update(raw)
            manifest["chunks"][-1]["count"] += 1
            count += 1
    finally:
        if stream is not None:
            stream.close()
            manifest["chunks"][-1]["sha256"] = digest.hexdigest()
    manifest["equation_count"] = count
    (directory / "equations.index.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def iter_equation_chunks(directory, verify=True):
    directory = Path(directory)
    index = json.loads((directory / "equations.index.json").read_text(encoding="utf-8"))
    total = 0
    for chunk in index["chunks"]:
        path = (directory / chunk["path"]).resolve()
        if not path.is_relative_to(directory.resolve()):
            raise ValueError("Equation chunk path escapes IR directory")
        if verify and hashlib.sha256(path.read_bytes()).hexdigest() != chunk["sha256"]:
            raise ValueError(f"Corrupted equation chunk: {path.name}")
        with path.open(encoding="utf-8") as stream:
            n = 0
            for line in stream:
                yield json.loads(line)
                n += 1
            if n != chunk["count"]:
                raise ValueError(f"Incorrect equation count: {path.name}")
            total += n
    if total != index["equation_count"]:
        raise ValueError("Incorrect total equation count")
