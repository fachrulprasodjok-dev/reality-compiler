from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reality_compiler.solver import solve
from reality_compiler.repair import find_minimal_relaxation

cases = sorted((ROOT / "eval" / "cases").glob("case_*.json"))
correct = 0

for p in cases:
    case = json.loads(p.read_text())
    result = solve(case["gold_constraints"])
    ok = result.status == case["gold"]["status"]
    correct += int(ok)
    print(f"{case['id']}: predicted={result.status:<5} gold={case['gold']['status']:<5} {'PASS' if ok else 'FAIL'}")
    if result.status == "UNSAT":
        print("  core:", ", ".join(result.unsat_core))
        repair = find_minimal_relaxation(case["gold_constraints"], result.unsat_core)
        if repair:
            print("  repair:", repair["repairs"][0]["proposal"])

print(f"\nGold-compiler sanity accuracy: {correct}/{len(cases)}")
