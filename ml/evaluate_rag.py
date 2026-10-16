"""Evaluate local PMFBY evidence retrieval using a reviewed JSONL query set.

Each line: {"question": "...", "expected_source_sha256": ["..."]}
This measures retrieval only; it does not validate legal correctness or claim eligibility.
"""
from __future__ import annotations
import argparse, json, statistics, sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
from typing import Any

# Configure the same knowledge directory as the backend before importing service.
def evaluate(path: Path, top_k: int = 5) -> dict[str, Any]:
    from app.knowledge_service import retrieve
    rows=[]
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            row=json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
        if not isinstance(row.get("question"), str) or not row["question"].strip():
            raise ValueError(f"Line {line_no} requires a non-empty question")
        expected=row.get("expected_source_sha256", [])
        if not isinstance(expected, list) or not all(isinstance(x, str) for x in expected):
            raise ValueError(f"Line {line_no}: expected_source_sha256 must be a list of strings")
        rows.append((row["question"], set(expected)))
    if not rows:
        raise ValueError("Evaluation set is empty")
    recalls=[]; reciprocal_ranks=[]; evaluated=0
    for question, expected in rows:
        if not expected:
            continue
        evaluated += 1
        results=retrieve(question, limit=top_k)
        found=[x.get("document_sha256", "") for x in results]
        hits=[i for i, checksum in enumerate(found, 1) if checksum in expected]
        recalls.append(1.0 if hits else 0.0)
        reciprocal_ranks.append(1.0 / hits[0] if hits else 0.0)
    return {
        "queries_total": len(rows), "queries_with_labels": evaluated, "top_k": top_k,
        "recall_at_k": round(statistics.mean(recalls), 4) if recalls else None,
        "mean_reciprocal_rank": round(statistics.mean(reciprocal_ranks), 4) if reciprocal_ranks else None,
        "warning": "Retrieval metrics only. Labels must be reviewed; scores do not establish legal correctness, applicability, or eligibility."
    }

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path, help="Reviewed JSONL retrieval evaluation set")
    parser.add_argument("--top-k", type=int, default=5)
    args=parser.parse_args()
    if not 1 <= args.top_k <= 10:
        parser.error("--top-k must be between 1 and 10")
    print(json.dumps(evaluate(args.dataset, args.top_k), indent=2))
