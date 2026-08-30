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
        "status": {
            "type": "string",
            "enum": [
                "SAT",
                "UNSAT",
            ],
        },
        "conflict_source_ids": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "explanation": {
            "type": "string",
        },
        "repair": {
            "type": [
                "string",
                "null",
            ],
        },
    },
    "required": [
        "status",
        "conflict_source_ids",
        "explanation",
        "repair",
    ],
    "additionalProperties": False,
}


INSTRUCTIONS = """
You are the direct-LLM baseline for a project feasibility
evaluation benchmark.

You receive only raw organizational evidence.

Determine whether all stated commitments, dates, policies,
dependencies, and requirements can simultaneously be true.

Return:

SAT
if the evidence is mutually feasible.

UNSAT
if the evidence contains a contradiction that makes the
plan impossible as stated.

For UNSAT cases:
- identify the source IDs involved in the contradiction
- provide a concise explanation
- propose a minimal practical repair if possible

For SAT cases:
- conflict_source_ids must be []
- repair must be null

Reason carefully about:
- deadlines
- fixed dates
- minimum delays
- ordering constraints
- explicit statements that two milestones are the same event

Do not assume unstated facts.
Do not invent dependencies.
Use only the supplied evidence.

Return the final judgment, not private chain-of-thought.
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
            "direct_baseline_v0_1.jsonl"
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
                "name": "direct_baseline_result",
                "strict": True,
                "schema": OUTPUT_SCHEMA,
            }
        },
        store=False,
    )

    latency_seconds = (
        time.perf_counter()
        - started
    )

    result = json.loads(
        response.output_text
    )

    predicted = result["status"]
    gold = case["gold"]["status"]

    return {
        "case_id": case["id"],
        "title": case["title"],
        "model": MODEL,
        "gold_status": gold,
        "predicted_status": predicted,
        "correct": predicted == gold,
        "conflict_source_ids": (
            result["conflict_source_ids"]
        ),
        "explanation": result["explanation"],
        "repair": result["repair"],
        "latency_seconds": round(
            latency_seconds,
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

    cases = sorted(
        cases_dir.glob("case_*.json")
    )

    client = OpenAI()

    correct = 0
    errors = 0
    total_latency = 0.0

    print(
        "\n=== DIRECT LLM BASELINE ==="
    )

    print(f"Model: {MODEL}")
    print(
        "Benchmark:",
        cases_dir.relative_to(ROOT),
    )
    print(f"Cases: {len(cases)}\n")

    with open(
        output_path,
        "w",
    ) as output_file:

        for index, path in enumerate(
            cases,
            start=1,
        ):
            try:
                with open(path) as f:
                    case = json.load(f)

                record = run_case(
                    client,
                    case,
                )

                if record["correct"]:
                    correct += 1

                total_latency += record[
                    "latency_seconds"
                ]

                verdict = (
                    "PASS"
                    if record["correct"]
                    else "FAIL"
                )

                print(
                    f"[{index}/{len(cases)}] "
                    f"{record['case_id']} "
                    f"gold="
                    f"{record['gold_status']} "
                    f"predicted="
                    f"{record['predicted_status']} "
                    f"{verdict} "
                    f"latency="
                    f"{record['latency_seconds']}s"
                )

            except Exception as exc:
                errors += 1

                record = {
                    "case_id": path.stem,
                    "model": MODEL,
                    "correct": False,
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                }

                print(
                    f"[{index}/{len(cases)}] "
                    f"{path.stem} ERROR: {exc}"
                )

            output_file.write(
                json.dumps(record)
                + "\n"
            )
            output_file.flush()

    total = len(cases)

    accuracy = (
        correct / total
        if total
        else 0
    )

    avg_latency = (
        total_latency / total
        if total
        else 0
    )

    print(
        "\n=== BASELINE RESULTS ==="
    )

    print(
        f"Correct: {correct}/{total}"
    )

    print(
        f"Accuracy: {accuracy:.1%}"
    )

    print(
        f"Errors: {errors}"
    )

    print(
        "Average latency: "
        f"{avg_latency:.3f}s"
    )

    print(
        "Results saved to:"
    )

    print(
        output_path.relative_to(ROOT)
    )


if __name__ == "__main__":
    main()