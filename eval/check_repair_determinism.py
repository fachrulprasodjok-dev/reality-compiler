import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.solver import solve
from src.reality_compiler.repair import find_minimal_relaxation
from src.reality_compiler.repair_policy import apply_repair_policy


RESULTS_PATH = (
    ROOT
    / "eval/results/"
    / "advanced_v0_4_same_event.jsonl"
)

REPEATS = 100


def normalized_repair(repair):
    if repair is None:
        return None

    return {
        "relaxation_count": repair.get(
            "relaxation_count"
        ),
        "repairs": repair.get(
            "repairs"
        ),
        "resulting_status": repair.get(
            "resulting_status"
        ),
        "model_dates": repair.get(
            "model_dates"
        ),
    }


def generate_repair(constraints):
    annotated = apply_repair_policy(
        constraints
    )

    result = solve(
        annotated
    )

    if result.status != "UNSAT":
        return None

    return find_minimal_relaxation(
        annotated,
        result.unsat_core,
    )


def main():
    records = []

    with open(RESULTS_PATH) as f:
        for line in f:
            if not line.strip():
                continue

            record = json.loads(line)

            if (
                record.get("gold_status")
                == "UNSAT"
            ):
                records.append(
                    record
                )

    stable_cases = 0

    print(
        "=== REPAIR ENGINE DETERMINISM ==="
    )

    print(
        f"UNSAT cases: {len(records)}"
    )

    print(
        f"Repeats per case: {REPEATS}"
    )

    print()

    for record in records:
        case_id = record[
            "case_id"
        ]

        constraints = record[
            "constraints"
        ]

        first = normalized_repair(
            generate_repair(
                constraints
            )
        )

        stable = True

        for _ in range(
            REPEATS - 1
        ):
            current = normalized_repair(
                generate_repair(
                    constraints
                )
            )

            if current != first:
                stable = False
                break

        if stable:
            stable_cases += 1

        repair_ids = []

        if first:
            repair_ids = [
                item.get(
                    "relax_constraint_id"
                )
                for item
                in first.get(
                    "repairs",
                    []
                )
            ]

        print(
            f"{case_id}: "
            f"{'STABLE' if stable else 'DRIFT'} "
            f"repair={repair_ids} "
            f"result="
            f"{first.get('resulting_status') if first else None}"
        )

    total_runs = (
        len(records)
        * REPEATS
    )

    print()
    print(
        "=== RESULTS ==="
    )

    print(
        "Stable repair cases: "
        f"{stable_cases}/{len(records)}"
    )

    print(
        "Deterministic rate: "
        f"{stable_cases / len(records):.1%}"
    )

    print(
        "Repair executions: "
        f"{total_runs}"
    )


if __name__ == "__main__":
    main()