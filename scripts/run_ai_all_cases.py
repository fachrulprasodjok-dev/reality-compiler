import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.extractor import (
    DEFAULT_MODEL,
    extract_constraints,
)
from src.reality_compiler.repair_policy import (
    apply_repair_policy,
)
from src.reality_compiler.repair import (
    find_minimal_relaxation,
)
from src.reality_compiler.solver import solve


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Reality Compiler against "
            "a versioned frozen benchmark."
        )
    )

    parser.add_argument(
        "--cases-dir",
        default="eval/cases",
        help=(
            "Directory containing case_*.json "
            "benchmark files."
        ),
    )

    parser.add_argument(
        "--output",
        default=(
            "eval/results/"
            "advanced_v0_2.jsonl"
        ),
        help="Where to save JSONL results.",
    )

    return parser.parse_args()


def run_case(case_path):
    with open(case_path) as f:
        case = json.load(f)

    # IMPORTANT:
    # The model receives ONLY raw sources.
    constraints = extract_constraints(
        case["sources"]
    )

    result = solve(
        constraints
    )

    repair = None

    if result.status == "UNSAT":
        repairable_constraints = (
            apply_repair_policy(
                constraints
            )
        )

        repair = (
            find_minimal_relaxation(
                repairable_constraints,
                result.unsat_core,
            )
        )

    predicted_status = (
        result.status
    )

    gold_status = (
        case["gold"]["status"]
    )

    return {
        "case_id": case["id"],
        "title": case["title"],
        "model": DEFAULT_MODEL,
        "gold_status": gold_status,
        "predicted_status": (
            predicted_status
        ),
        "correct": (
            predicted_status
            == gold_status
        ),
        "constraints": constraints,
        "unsat_core": (
            result.unsat_core
        ),
        "repair": repair,
    }


def main():
    args = parse_args()

    cases_dir = (
        ROOT / args.cases_dir
    )

    output_path = (
        ROOT / args.output
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    case_paths = sorted(
        cases_dir.glob(
            "case_*.json"
        )
    )

    total = len(
        case_paths
    )

    correct = 0
    errors = 0

    print(
        "\n=== REALITY COMPILER "
        "MODEL-BACKED EVALUATION ==="
    )

    print(
        "Extraction: model-backed / probabilistic"
    )

    print(
        "Formal engine: deterministic after extraction"
    )

    print(
        f"Model: {DEFAULT_MODEL}"
    )

    print(
        "Benchmark:",
        cases_dir.relative_to(
            ROOT
        ),
    )

    print(
        f"Cases: {total}\n"
    )

    with open(
        output_path,
        "w",
    ) as output_file:

        for index, case_path in enumerate(
            case_paths,
            start=1,
        ):
            try:
                record = run_case(
                    case_path
                )

                if record["correct"]:
                    correct += 1

                verdict = (
                    "PASS"
                    if record["correct"]
                    else "FAIL"
                )

                print(
                    f"[{index}/{total}] "
                    f"{record['case_id']} "
                    f"gold="
                    f"{record['gold_status']} "
                    f"predicted="
                    f"{record['predicted_status']} "
                    f"{verdict}"
                )

            except Exception as exc:
                errors += 1

                record = {
                    "case_id": (
                        case_path.stem
                    ),
                    "model": (
                        DEFAULT_MODEL
                    ),
                    "correct": False,
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                }

                print(
                    f"[{index}/{total}] "
                    f"{case_path.stem} "
                    f"ERROR: {exc}"
                )

            output_file.write(
                json.dumps(record)
                + "\n"
            )

            output_file.flush()

    accuracy = (
        correct / total
        if total
        else 0
    )

    print(
        "\n=== RESULTS ==="
    )

    print(
        f"Correct: {correct}/{total}"
    )

    print(
        "Feasibility accuracy: "
        f"{accuracy:.1%}"
    )

    print(
        f"Errors: {errors}"
    )

    print(
        "Results saved to:"
    )

    print(
        output_path.relative_to(
            ROOT
        )
    )


if __name__ == "__main__":
    main()