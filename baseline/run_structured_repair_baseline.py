import argparse
import json
import sys
import time
from pathlib import Path

from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


MODEL = "gpt-5.6-luna"


OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "source_id": {
            "type": "string",
        },
        "original_date": {
            "type": "string",
        },
        "new_date": {
            "type": "string",
        },
        "explanation": {
            "type": "string",
        },
    },
    "required": [
        "source_id",
        "original_date",
        "new_date",
        "explanation",
    ],
    "additionalProperties": False,
}


INSTRUCTIONS = """
You are a repair baseline for an organizational
feasibility benchmark.

You receive raw source evidence for a plan that is known
to be infeasible.

Your task is to propose exactly ONE concrete date change
that is sufficient to make the complete plan feasible.

Requirements:

- Change exactly one explicitly stated date.
- Choose the smallest practical date adjustment you can.
- Do not propose multiple alternatives.
- Do not change or ignore any other requirement.
- Use only the supplied evidence.
- Do not assume unstated facts.
- source_id must identify the source containing the date
  you want changed.
- original_date must exactly match the date in that source.
- new_date must be an ISO date YYYY-MM-DD.
- The proposed single change should make all supplied
  commitments mutually feasible.

Return only the structured result.
"""


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cases-dir",
        default="eval/cases_v0_3",
    )

    parser.add_argument(
        "--output",
        default=(
            "baseline/"
            "structured_repair_baseline_v0_1.jsonl"
        ),
    )

    return parser.parse_args()


def run_case(client, case):
    started = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=json.dumps(
            {
                "sources": case["sources"],
            },
            indent=2,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "structured_repair",
                "strict": True,
                "schema": OUTPUT_SCHEMA,
            }
        },
        store=False,
    )

    latency = (
        time.perf_counter()
        - started
    )

    repair = json.loads(
        response.output_text
    )

    return {
        "case_id": case["id"],
        "title": case["title"],
        "model": MODEL,
        "repair": repair,
        "latency_seconds": round(
            latency,
            3,
        ),
    }


def main():
    args = parse_args()

    cases_dir = ROOT / args.cases_dir
    output_path = ROOT / args.output

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    case_paths = sorted(
        cases_dir.glob("case_*.json")
    )

    client = OpenAI()

    unsat_cases = []

    for path in case_paths:
        with open(path) as f:
            case = json.load(f)

        if case["gold"]["status"] == "UNSAT":
            unsat_cases.append(
                (path, case)
            )

    print(
        "\n=== STRUCTURED REPAIR BASELINE ==="
    )

    print(f"Model: {MODEL}")
    print(
        f"UNSAT cases: {len(unsat_cases)}\n"
    )

    with open(
        output_path,
        "w",
    ) as output_file:

        for index, (_, case) in enumerate(
            unsat_cases,
            start=1,
        ):
            try:
                record = run_case(
                    client,
                    case,
                )

                repair = record["repair"]

                print(
                    f"[{index}/{len(unsat_cases)}] "
                    f"{record['case_id']} "
                    f"{repair['source_id']} "
                    f"{repair['original_date']} "
                    f"-> "
                    f"{repair['new_date']} "
                    f"latency="
                    f"{record['latency_seconds']}s"
                )

            except Exception as exc:
                record = {
                    "case_id": case["id"],
                    "model": MODEL,
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                }

                print(
                    f"[{index}/{len(unsat_cases)}] "
                    f"{case['id']} "
                    f"ERROR: {exc}"
                )

            output_file.write(
                json.dumps(record)
                + "\n"
            )

            output_file.flush()

    print(
        "\nResults saved to:"
    )

    print(
        output_path.relative_to(ROOT)
    )


if __name__ == "__main__":
    main()