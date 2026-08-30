import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.solver import solve


RESULTS_PATH = (
    ROOT
    / "eval/results/"
    / "advanced_v0_4_same_event.jsonl"
)


REPEATS = 100


def normalized_result(result):
    return {
        "status": result.status,
        "unsat_core": list(
            result.unsat_core
        ),
    }


def main():
    records = []

    with open(RESULTS_PATH) as f:
        for line in f:
            if line.strip():
                records.append(
                    json.loads(line)
                )

    total_runs = 0
    stable_cases = 0

    print(
        "=== REALITY ENGINE DETERMINISM ==="
    )

    print(
        f"Cases: {len(records)}"
    )

    print(
        f"Repeats per case: {REPEATS}"
    )

    print()

    for record in records:
        case_id = record["case_id"]

        constraints = record[
            "constraints"
        ]

        first = normalized_result(
            solve(constraints)
        )

        stable = True

        for _ in range(
            REPEATS - 1
        ):
            current = normalized_result(
                solve(constraints)
            )

            total_runs += 1

            if current != first:
                stable = False
                break

        total_runs += 1

        if stable:
            stable_cases += 1

        print(
            f"{case_id}: "
            f"{'STABLE' if stable else 'DRIFT'} "
            f"status={first['status']} "
            f"core={first['unsat_core']}"
        )

    total_expected_runs = (
        len(records)
        * REPEATS
    )

    print()
    print(
        "=== RESULTS ==="
    )

    print(
        "Stable cases: "
        f"{stable_cases}/{len(records)}"
    )

    print(
        "Deterministic rate: "
        f"{stable_cases / len(records):.1%}"
    )

    print(
        "Solver executions: "
        f"{total_expected_runs}"
    )


if __name__ == "__main__":
    main()