import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def gold_conflict_sources(case):
    if case["gold"]["status"] != "UNSAT":
        return set()

    conflict_ids = set(
        case["gold"].get(
            "conflict_ids",
            [],
        )
    )

    return {
        constraint["source_id"]
        for constraint
        in case["gold_constraints"]
        if constraint["id"]
        in conflict_ids
    }


def reality_conflict_sources(record):
    core_ids = set(
        record.get(
            "unsat_core",
            [],
        )
    )

    return {
        constraint["source_id"]
        for constraint
        in record.get(
            "constraints",
            []
        )
        if constraint["id"]
        in core_ids
    }


def score_set(predicted, gold):
    intersection = (
        predicted & gold
    )

    precision = (
        len(intersection)
        / len(predicted)
        if predicted
        else (
            1.0
            if not gold
            else 0.0
        )
    )

    recall = (
        len(intersection)
        / len(gold)
        if gold
        else 1.0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall
        else 0.0
    )

    return {
        "exact": predicted == gold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "extra": len(
            predicted - gold
        ),
        "missing": len(
            gold - predicted
        ),
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
            "direct_baseline_v0_1.jsonl"
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
            "localization_comparison_v0_1.json"
        ),
    )

    return parser.parse_args()


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

    rows = []

    systems = {
        "direct_llm": [],
        "reality_compiler": [],
    }

    case_paths = sorted(
        cases_dir.glob(
            "case_*.json"
        )
    )

    for path in case_paths:
        with open(path) as f:
            case = json.load(f)

        if (
            case["gold"]["status"]
            != "UNSAT"
        ):
            continue

        case_id = case["id"]

        gold_sources = (
            gold_conflict_sources(
                case
            )
        )

        baseline_sources = set(
            baseline[
                case_id
            ].get(
                "conflict_source_ids",
                [],
            )
        )

        reality_sources = (
            reality_conflict_sources(
                reality[case_id]
            )
        )

        baseline_score = score_set(
            baseline_sources,
            gold_sources,
        )

        reality_score = score_set(
            reality_sources,
            gold_sources,
        )

        systems[
            "direct_llm"
        ].append(
            baseline_score
        )

        systems[
            "reality_compiler"
        ].append(
            reality_score
        )

        rows.append(
            {
                "case_id": case_id,
                "gold_sources": sorted(
                    gold_sources
                ),
                "direct_llm_sources": (
                    sorted(
                        baseline_sources
                    )
                ),
                "direct_llm_score": (
                    baseline_score
                ),
                "reality_sources": (
                    sorted(
                        reality_sources
                    )
                ),
                "reality_score": (
                    reality_score
                ),
            }
        )

        print(
            f"{case_id}:"
        )

        print(
            "  gold:",
            ", ".join(
                sorted(gold_sources)
            ),
        )

        print(
            "  direct:",
            ", ".join(
                sorted(
                    baseline_sources
                )
            ),
            "EXACT"
            if baseline_score["exact"]
            else "MISS",
        )

        print(
            "  reality:",
            ", ".join(
                sorted(
                    reality_sources
                )
            ),
            "EXACT"
            if reality_score["exact"]
            else "MISS",
        )

    summary = {}

    for name, scores in (
        systems.items()
    ):
        count = len(scores)

        exact = sum(
            1
            for score in scores
            if score["exact"]
        )

        summary[name] = {
            "cases": count,
            "exact_matches": exact,
            "exact_match_rate": (
                exact / count
                if count
                else 0
            ),
            "mean_precision": (
                sum(
                    s["precision"]
                    for s in scores
                ) / count
                if count
                else 0
            ),
            "mean_recall": (
                sum(
                    s["recall"]
                    for s in scores
                ) / count
                if count
                else 0
            ),
            "mean_f1": (
                sum(
                    s["f1"]
                    for s in scores
                ) / count
                if count
                else 0
            ),
            "total_extra_sources": sum(
                s["extra"]
                for s in scores
            ),
            "total_missing_sources": sum(
                s["missing"]
                for s in scores
            ),
        }

    output = {
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
        "\n=== CONFLICT LOCALIZATION ==="
    )

    for name in [
        "direct_llm",
        "reality_compiler",
    ]:
        result = summary[name]

        print(
            f"\n{name}:"
        )

        print(
            "Exact conflict sets: "
            f"{result['exact_matches']}/"
            f"{result['cases']} "
            f"({result['exact_match_rate']:.1%})"
        )

        print(
            "Mean precision: "
            f"{result['mean_precision']:.1%}"
        )

        print(
            "Mean recall: "
            f"{result['mean_recall']:.1%}"
        )

        print(
            "Mean F1: "
            f"{result['mean_f1']:.1%}"
        )

        print(
            "Extra sources: "
            f"{result['total_extra_sources']}"
        )

        print(
            "Missing sources: "
            f"{result['total_missing_sources']}"
        )

    print(
        "\nSaved to:"
    )

    print(
        output_path.relative_to(ROOT)
    )


if __name__ == "__main__":
    main()