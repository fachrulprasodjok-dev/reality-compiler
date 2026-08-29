from pathlib import Path
import json, sys, unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reality_compiler.solver import solve
from reality_compiler.repair import find_minimal_relaxation

def load_case(n):
    return json.loads((ROOT / "eval" / "cases" / f"case_{n:02}.json").read_text())

class RealityCompilerSolverTests(unittest.TestCase):
    def test_challenge_is_unsat(self):
        case = load_case(2)
        result = solve(case["gold_constraints"])
        self.assertEqual(result.status, "UNSAT")
        self.assertEqual(set(result.unsat_core), set(case["gold"]["conflict_ids"]))

    def test_feasible_case_is_sat(self):
        case = load_case(1)
        self.assertEqual(solve(case["gold_constraints"]).status, "SAT")

    def test_challenge_has_one_change_repair(self):
        case = load_case(2)
        result = solve(case["gold_constraints"])
        repair = find_minimal_relaxation(case["gold_constraints"], result.unsat_core)
        self.assertIsNotNone(repair)
        self.assertEqual(repair["relaxation_count"], 1)
        self.assertEqual(repair["resulting_status"], "SAT")

    def test_all_gold_cases(self):
        for n in range(1, 13):
            case = load_case(n)
            with self.subTest(case=n):
                self.assertEqual(
                    solve(case["gold_constraints"]).status,
                    case["gold"]["status"]
                )

if __name__ == "__main__":
    unittest.main()
