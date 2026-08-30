import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.canonicalizer import (
    canonicalize_constraints,
)
from src.reality_compiler.extractor import (
    DEFAULT_MODEL,
    extract_constraints,
)
from src.reality_compiler.solver import solve


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Predefined Case 04 semantic extraction "
            "robustness probe."
        )
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--case",
        default="eval/cases_v0_3/case_04.json",
    )

    parser.add_argument(
        "--output",
        default=(
            "eval/results/"
            "CASE04_SEMANTIC_ROBUSTNESS_v0_1.json"
        ),
    )

    return parser.parse_args()


def formalization_signature(constraints):
    payload = json.dumps(
        constraints,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()[:12]


def has_semantic_coverage(constraints):
    """
    Case-04-specific check.

    After deterministic same_event canonicalization,
    the exact security-review date and the
    security-approval-before-release constraint must
    refer to the same canonical event.

    This accepts either:
    - explicit same_event, or
    - direct reuse of the same event symbol.
    """

    normalized = canonicalize_constraints(
        constraints
    )

    review_events = {
        c["event"]
        for c in normalized
        if (
            c.get("kind") == "fixed_date"
            and c.get("source_id") == "S1"
            and c.get("date") == "2026-10-16"
        )
    }

    approval_events = {
        c["event"]
        for c in normalized
        if (
            c.get("kind") == "before_or_same"
            and c.get("source_id") == "P1"
            and c.get("ref") == "release"
        )
    }

    return bool(
        review_events
        & approval_events
    )


def main():
    args = parse_args()

    case_path = ROOT / args.case
    output_path = ROOT / args.output

    with open(case_path) as f:
        case = json.load(f)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    print(
        "\n=== CASE 04 SEMANTIC "
        "ROBUSTNESS PROBE ==="
    )

    print(f"Model: {DEFAULT_MODEL}")
    print(f"Runs: {args.runs}")
    print(
        "Protocol: no retries, "
        "no manual correction\n"
    )

    for run in range(
        1,
        args.runs + 1,
    ):
        try:
            constraints = extract_constraints(
                case["sources"]
            )

            result = solve(
                constraints
            )

            explicit_same_event = any(
                c.get("kind") == "same_event"
                for c in constraints
            )

            semantic_complete = (
                has_semantic_coverage(
                    constraints
                )
            )

            signature = (
                formalization_signature(
                    constraints
                )
            )

            correct = (
                result.status
                == case["gold"]["status"]
            )

            row = {
                "run": run,
                "status": result.status,
                "correct": correct,
                "explicit_same_event": (
                    explicit_same_event
                ),
                "semantic_complete": (
                    semantic_complete
                ),
                "signature": signature,
                "constraints": constraints,
                "unsat_core": (
                    result.unsat_core
                ),
            }

            print(
                f"[{run}/{args.runs}] "
                f"status={result.status} "
                f"correct={correct} "
                f"same_event="
                f"{explicit_same_event} "
                f"coverage="
                f"{semantic_complete} "
                f"signature={signature}"
            )

        except Exception as exc:
            row = {
                "run": run,
                "correct": False,
                "error": (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            }

            print(
                f"[{run}/{args.runs}] "
                f"ERROR: {exc}"
            )

        rows.append(row)

    completed = [
        r for r in rows
        if "error" not in r
    ]

    signatures = {
        r["signature"]
        for r in completed
    }

    summary = {
        "runs": args.runs,
        "completed": len(completed),
        "errors": (
            args.runs
            - len(completed)
        ),
        "correct_final_status": sum(
            bool(r.get("correct"))
            for r in completed
        ),
        "explicit_same_event": sum(
            bool(
                r.get(
                    "explicit_same_event"
                )
            )
            for r in completed
        ),
        "semantic_complete": sum(
            bool(
                r.get(
                    "semantic_complete"
                )
            )
            for r in completed
        ),
        "distinct_formalizations": len(
            signatures
        ),
    }

    artifact = {
        "case_id": case["id"],
        "model": DEFAULT_MODEL,
        "protocol": {
            "independent_runs": (
                args.runs
            ),
            "retries": 0,
            "manual_corrections": 0,
            "model_receives_gold": False,
        },
        "summary": summary,
        "rows": rows,
    }

    with open(
        output_path,
        "w",
    ) as f:
        json.dump(
            artifact,
            f,
            indent=2,
        )

    print(
        "\n=== RESULTS ==="
    )

    print(
        "Correct final status: "
        f"{summary['correct_final_status']}"
        f"/{args.runs}"
    )

    print(
        "Explicit same_event: "
        f"{summary['explicit_same_event']}"
        f"/{args.runs}"
    )

    print(
        "Semantic coverage: "
        f"{summary['semantic_complete']}"
        f"/{args.runs}"
    )

    print(
        "Distinct formalizations: "
        f"{summary['distinct_formalizations']}"
    )

    print(
        f"Errors: {summary['errors']}"
    )

    print(
        "\nSaved to:"
    )

    print(
        output_path.relative_to(
            ROOT
        )
    )


if __name__ == "__main__":
    main()
