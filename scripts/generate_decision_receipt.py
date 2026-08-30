import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.receipt import (
    render_html,
    render_markdown,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a user-facing Reality "
            "Compiler decision receipt."
        )
    )

    parser.add_argument(
        "--case",
        required=True,
    )

    parser.add_argument(
        "--results",
        required=True,
    )

    parser.add_argument(
        "--markdown-output",
        required=True,
    )

    parser.add_argument(
        "--html-output",
        required=True,
    )

    return parser.parse_args()


def load_result(path, case_id):
    with open(path) as f:
        for line in f:
            record = json.loads(
                line
            )

            if (
                record.get("case_id")
                == case_id
            ):
                return record

    raise ValueError(
        f"No result found for {case_id}"
    )


def main():
    args = parse_args()

    case_path = ROOT / args.case
    results_path = ROOT / args.results

    with open(case_path) as f:
        case = json.load(f)

    record = load_result(
        results_path,
        case["id"],
    )

    markdown = render_markdown(
        case,
        record,
    )

    html = render_html(
        case,
        record,
    )

    markdown_path = (
        ROOT / args.markdown_output
    )

    html_path = (
        ROOT / args.html_output
    )

    markdown_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    html_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    markdown_path.write_text(
        markdown,
        encoding="utf-8",
    )

    html_path.write_text(
        html,
        encoding="utf-8",
    )

    print(
        "Decision receipt generated:"
    )

    print(
        markdown_path.relative_to(
            ROOT
        )
    )

    print(
        html_path.relative_to(
            ROOT
        )
    )


if __name__ == "__main__":
    main()