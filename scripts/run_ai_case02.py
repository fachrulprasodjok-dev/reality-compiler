import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.reality_compiler.extractor import extract_constraints
from src.reality_compiler.solver import solve
from src.reality_compiler.repair import find_minimal_relaxation
from src.reality_compiler.repair_policy import apply_repair_policy

CASE_PATH = "eval/cases/case_02.json"


with open(CASE_PATH) as f:
    case = json.load(f)


print("\n=== REALITY COMPILER ===")
print(f"Case: {case['title']}")


# 1. Give the AI ONLY the raw evidence.
constraints = extract_constraints(case["sources"])
repairable_constraints = apply_repair_policy(
    constraints
)


print("\n=== AI EXTRACTED CONSTRAINTS ===")

for constraint in constraints:
    print(
        f"{constraint['id']}: "
        f"{constraint['kind']} | "
        f"{constraint['description']}"
    )


# 2. Formal feasibility proof.
result = solve(constraints)


print("\n=== REALITY ENGINE ===")
print("STATUS:", result.status)


if result.status == "UNSAT":

    print(
        "UNSAT CORE:",
        ", ".join(result.unsat_core),
    )

    # 3. Search for smallest supported repair.
    repair = find_minimal_relaxation(
        repairable_constraints,
        result.unsat_core,
    )

    print("\n=== MINIMAL REPAIR ===")

    if repair:
        print(
            "CHANGES REQUIRED:",
            repair["relaxation_count"],
        )

        for item in repair["repairs"]:
            print(
                "REPAIR:",
                item["proposal"],
            )

        print(
            "AFTER REPAIR:",
            repair["resulting_status"],
        )

    else:
        print(
            "No supported minimal repair found."
        )