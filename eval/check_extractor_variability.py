import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.extractor import extract_constraints
from src.reality_compiler.solver import solve


CASE_PATH = (
    ROOT
    / "eval/cases_v0_3/case_04.json"
)

OUTPUT_PATH = (
    ROOT
    / "eval/results/"
    / "EXTRACTOR_VARIABILITY_case04_v0_1.json"
)

REPEATS = 5


def semantic_view(constraints):
    keys = [
        "kind",
        "event",
        "ref",
        "date",
        "days",
        "source_id",
    ]

    rows = []

    for constraint in constraints:
        row = {
            key: constraint[key]
            for key in keys
            if key in constraint
        }

        rows.append(row)

    rows.sort(
        key=lambda item: json.dumps(
            item,
            sort_keys=True,
        )
    )

    return rows


def signature(view):
    payload = json.dumps(
        view,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        payload.encode()
    ).hexdigest()[:10]


def main():
    with open(CASE_PATH) as f:
        case = json.load(f)

    gold_status = case["gold"]["status"]

    runs = []
    signatures = []
    statuses = []

    print(
        "=== EXTRACTOR VARIABILITY ==="
    )
    print("Case: case_04")
    print(f"Repeats: {REPEATS}")
    print(f"Gold status: {gold_status}")
    print()

    for index in range(
        1,
        REPEATS + 1,
    ):
        constraints = extract_constraints(
            case["sources"]
        )

        result = solve(
            constraints
        )

        view = semantic_view(
            constraints
        )

        sig = signature(
            view
        )

        same_event = [
            {
                "event": c.get("event"),
                "ref": c.get("ref"),
            }
            for c in constraints
            if c.get("kind")
            == "same_event"
        ]

        signatures.append(sig)
        statuses.append(
            result.status
        )

        runs.append(
            {
                "run": index,
                "signature": sig,
                "constraints": constraints,
                "semantic_view": view,
                "same_event": same_event,
                "status": result.status,
                "unsat_core": (
                    result.unsat_core
                ),
            }
        )

        print(
            f"[{index}/{REPEATS}] "
            f"signature={sig} "
            f"status={result.status} "
            f"same_event={same_event}"
        )

    unique_signatures = len(
        set(signatures)
    )

    unique_statuses = sorted(
        set(statuses)
    )

    correct_runs = sum(
        1
        for status in statuses
        if status == gold_status
    )

    same_event_runs = sum(
        1
        for run in runs
        if run["same_event"]
    )

    output = {
        "case_id": "case_04",
        "repeats": REPEATS,
        "gold_status": gold_status,
        "runs": runs,
        "summary": {
            "unique_formalizations": (
                unique_signatures
            ),
            "unique_statuses": (
                unique_statuses
            ),
            "correct_runs": (
                correct_runs
            ),
            "same_event_runs": (
                same_event_runs
            ),
        },
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_PATH,
        "w",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
        )

    print()
    print(
        "=== RESULTS ==="
    )

    print(
        "Unique formalizations: "
        f"{unique_signatures}/{REPEATS}"
    )

    print(
        "same_event emitted: "
        f"{same_event_runs}/{REPEATS}"
    )

    print(
        "Correct final status: "
        f"{correct_runs}/{REPEATS}"
    )

    print(
        "Unique final statuses: "
        f"{unique_statuses}"
    )

    print()
    print(
        "Saved to:"
    )

    print(
        OUTPUT_PATH.relative_to(
            ROOT
        )
    )


if __name__ == "__main__":
    main()