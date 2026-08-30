import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.solver import solve


DATE_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}"
)


def load_jsonl(path):
    records = {}

    with open(path) as f:
        for line in f:
            if not line.strip():
                continue

            record = json.loads(line)

            records[
                record["case_id"]
            ] = record

    return records


def apply_source_date_edit(
    constraints,
    source_id,
    original_date,
    new_date,
):
    edited = []
    matches = 0

    for constraint in constraints:
        item = dict(constraint)

        if (
            item.get("source_id")
            == source_id
            and item.get("date")
            == original_date
        ):
            item["date"] = new_date
            matches += 1

        edited.append(item)

    return edited, matches


def verify_edit(
    constraints,
    source_id,
    original_date,
    new_date,
):
    edited, matches = (
        apply_source_date_edit(
            constraints,
            source_id,
            original_date,
            new_date,
        )
    )

    if matches == 0:
        return {
            "matches": 0,
            "resulting_status": None,
            "verified": False,
        }

    result = solve(edited)

    return {
        "matches": matches,
        "resulting_status": result.status,
        "verified": (
            result.status == "SAT"
        ),
    }


def find_direction_minimum(
    constraints,
    source_id,
    original_date,
    proposed_date,
):
    old = date.fromisoformat(
        original_date
    )

    new = date.fromisoformat(
        proposed_date
    )

    delta_days = (
        new - old
    ).days

    if delta_days == 0:
        return {
            "proposed_days_moved": 0,
            "minimum_days_moved": None,
            "minimum_date": None,
            "boundary_minimal": False,
        }

    direction = (
        1
        if delta_days > 0
        else -1
    )

    proposed_days = abs(
        delta_days
    )

    minimum_date = None
    minimum_days = None

    for days in range(
        1,
        proposed_days + 1,
    ):
        candidate = (
            old
            + timedelta(
                days=direction * days
            )
        )

        verification = verify_edit(
            constraints,
            source_id,
            original_date,
            candidate.isoformat(),
        )

        if verification["verified"]:
            minimum_date = (
                candidate.isoformat()
            )
            minimum_days = days
            break

    return {
        "proposed_days_moved": (
            proposed_days
        ),
        "minimum_days_moved": (
            minimum_days
        ),
        "minimum_date": (
            minimum_date
        ),
        "boundary_minimal": (
            minimum_days
            == proposed_days
            if minimum_days is not None
            else False
        ),
    }


def reality_repair_edit(record):
    repair = record.get(
        "repair"
    )

    if not repair:
        return None

    repairs = repair.get(
        "repairs",
        []
    )

    if len(repairs) != 1:
        return None

    item = repairs[0]

    constraint_id = item[
        "relax_constraint_id"
    ]

    target = None

    for constraint in record.get(
        "constraints",
        [],
    ):
        if (
            constraint.get("id")
            == constraint_id
        ):
            target = constraint
            break

    if not target:
        return None

    original_date = target.get(
        "date"
    )

    if not original_date:
        return None

    source_id = item.get(
        "source_id"
    )

    model_dates = repair.get(
        "model_dates",
        {}
    )

    new_date = model_dates.get(
        target.get("event")
    )

    if not new_date:
        dates = DATE_RE.findall(
            item.get(
                "proposal",
                "",
            )
        )

        if dates:
            new_date = dates[-1]

    if not new_date:
        return None

    return {
        "source_id": source_id,
        "original_date": original_date,
        "new_date": new_date,
        "constraint_id": constraint_id,
    }


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cases-dir",
        default="eval/cases_v0_3",
    )

    parser.add_argument(
        "--baseline",
        default=(
            "baseline/"
            "structured_repair_baseline_v0_1.jsonl"
        ),
    )

    parser.add_argument(
        "--reality",
        default=(
            "eval/results/"
            "advanced_v0_4_same_event.jsonl"
        ),
    )

    parser.add_argument(
        "--output",
        default=(
            "eval/results/"
            "repair_verification_v0_1.json"
        ),
    )

    return parser.parse_args()


def evaluate_repair(
    constraints,
    edit,
):
    if not edit:
        return {
            "verified": False,
            "reason": (
                "No machine-applicable "
                "single-date repair."
            ),
        }

    verification = verify_edit(
        constraints,
        edit["source_id"],
        edit["original_date"],
        edit["new_date"],
    )

    minimality = (
        find_direction_minimum(
            constraints,
            edit["source_id"],
            edit["original_date"],
            edit["new_date"],
        )
    )

    return {
        **edit,
        **verification,
        **minimality,
    }


def summarize(results):
    count = len(results)

    verified = sum(
        1
        for result in results
        if result.get("verified")
    )

    minimal = sum(
        1
        for result in results
        if result.get(
            "boundary_minimal"
        )
    )

    proposed_moves = [
        result[
            "proposed_days_moved"
        ]
        for result in results
        if result.get(
            "proposed_days_moved"
        ) is not None
    ]

    return {
        "cases": count,
        "verified_repairs": verified,
        "verified_rate": (
            verified / count
            if count
            else 0
        ),
        "boundary_minimal_repairs": (
            minimal
        ),
        "boundary_minimal_rate": (
            minimal / count
            if count
            else 0
        ),
        "mean_days_moved": (
            sum(proposed_moves)
            / len(proposed_moves)
            if proposed_moves
            else 0
        ),
    }


def main():
    args = parse_args()

    cases_dir = (
        ROOT / args.cases_dir
    )

    baseline = load_jsonl(
        ROOT / args.baseline
    )

    reality = load_jsonl(
        ROOT / args.reality
    )

    direct_results = []
    reality_results = []
    rows = []

    for path in sorted(
        cases_dir.glob(
            "case_*.json"
        )
    ):
        with open(path) as f:
            case = json.load(f)

        if (
            case["gold"]["status"]
            != "UNSAT"
        ):
            continue

        case_id = case["id"]

        gold_constraints = (
            case["gold_constraints"]
        )

        original_result = solve(
            gold_constraints
        )

        if original_result.status != "UNSAT":
            raise RuntimeError(
                f"{case_id}: gold constraints "
                "do not solve to UNSAT."
            )

        baseline_record = baseline[
            case_id
        ]

        baseline_edit = (
            baseline_record.get(
                "repair"
            )
        )

        direct_result = (
            evaluate_repair(
                gold_constraints,
                baseline_edit,
            )
        )

        reality_edit = (
            reality_repair_edit(
                reality[case_id]
            )
        )

        reality_result = (
            evaluate_repair(
                gold_constraints,
                reality_edit,
            )
        )

        direct_results.append(
            direct_result
        )

        reality_results.append(
            reality_result
        )

        rows.append(
            {
                "case_id": case_id,
                "direct_llm": (
                    direct_result
                ),
                "reality_compiler": (
                    reality_result
                ),
            }
        )

        print(f"\n{case_id}:")

        for name, result in [
            (
                "direct",
                direct_result,
            ),
            (
                "reality",
                reality_result,
            ),
        ]:
            if (
                "source_id"
                not in result
            ):
                print(
                    f"  {name}: "
                    "UNVERIFIABLE"
                )
                continue

            print(
                f"  {name}: "
                f"{result['source_id']} "
                f"{result['original_date']} "
                f"-> {result['new_date']} "
                f"result="
                f"{result['resulting_status']} "
                f"verified="
                f"{result['verified']} "
                f"minimal="
                f"{result['boundary_minimal']}"
            )

            if (
                result.get(
                    "minimum_date"
                )
                and not result.get(
                    "boundary_minimal"
                )
            ):
                print(
                    "    nearest SAT date "
                    "in same direction: "
                    f"{result['minimum_date']}"
                )

    summary = {
        "direct_llm": summarize(
            direct_results
        ),
        "reality_compiler": summarize(
            reality_results
        ),
    }

    output = {
        "definition": {
            "verified_repair": (
                "Applying the proposed "
                "single source-date edit "
                "to the frozen gold formal "
                "constraints results in SAT."
            ),
            "boundary_minimal": (
                "No smaller day movement "
                "on that same source-date "
                "in the same direction "
                "produces SAT."
            ),
        },
        "rows": rows,
        "summary": summary,
    }

    output_path = (
        ROOT / args.output
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
        )

    print(
        "\n=== REPAIR VERIFICATION ==="
    )

    for name in [
        "direct_llm",
        "reality_compiler",
    ]:
        result = summary[name]

        print(f"\n{name}:")

        print(
            "Verified SAT repairs: "
            f"{result['verified_repairs']}/"
            f"{result['cases']} "
            f"({result['verified_rate']:.1%})"
        )

        print(
            "Boundary-minimal repairs: "
            f"{result['boundary_minimal_repairs']}/"
            f"{result['cases']} "
            f"({result['boundary_minimal_rate']:.1%})"
        )

        print(
            "Mean absolute days moved: "
            f"{result['mean_days_moved']:.2f}"
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