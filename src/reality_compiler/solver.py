from dataclasses import dataclass
from typing import Dict, List, Any, Tuple
from .date_utils import to_day, from_day
from .canonicalizer import canonicalize_constraints

ZERO = "__ZERO__"

@dataclass
class SolveResult:
    status: str
    unsat_core: List[str]
    model_dates: Dict[str, str]

def _event_names(constraints: List[Dict[str, Any]]) -> List[str]:
    names = {ZERO}
    for c in constraints:
        if c.get("event"):
            names.add(c["event"])
        if c.get("ref"):
            names.add(c["ref"])
    return sorted(names)

def _edges_for_constraint(c: Dict[str, Any]) -> List[Tuple[str, str, int]]:
    """
    Difference constraints are represented as:
        x_v <= x_u + weight
    encoded by edge (u, v, weight).
    """
    kind = c["kind"]
    e = c.get("event")

    if kind == "deadline":
        # event <= date
        return [(ZERO, e, to_day(c["date"]))]

    if kind == "earliest":
        # event >= date  ->  ZERO - event <= -date
        return [(e, ZERO, -to_day(c["date"]))]

    if kind == "fixed_date":
        d = to_day(c["date"])
        # event <= d AND event >= d
        return [(ZERO, e, d), (e, ZERO, -d)]

    if kind == "after_days":
        # event >= ref + days  -> ref - event <= -days
        return [(e, c["ref"], -int(c["days"]))]

    if kind == "before_or_same":
        # event <= ref
        return [(c["ref"], e, 0)]

    raise ValueError(f"Unsupported constraint kind: {kind}")

def _is_feasible(constraints: List[Dict[str, Any]]):
    nodes = _event_names(constraints)
    edges = []
    for c in constraints:
        edges.extend(_edges_for_constraint(c))

    # Super-source initialization at 0 for all nodes is equivalent to
    # adding zero-weight edges from a super source.
    dist = {n: 0 for n in nodes}

    # Bellman-Ford negative-cycle test.
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in edges:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    for u, v, w in edges:
        if dist[v] > dist[u] + w:
            return False, {}

    # Shift so ZERO becomes 0; only differences matter.
    shift = dist[ZERO]
    normalized = {n: dist[n] - shift for n in nodes}
    return True, normalized

def _minimal_unsat_core(constraints: List[Dict[str, Any]]) -> List[str]:
    feasible, _ = _is_feasible(constraints)
    if feasible:
        return []

    core = list(constraints)
    i = 0
    while i < len(core):
        candidate = core[:i] + core[i+1:]
        candidate_feasible, _ = _is_feasible(candidate)
        if not candidate_feasible:
            core = candidate
        else:
            i += 1
    return [c["id"] for c in core]

def solve(constraints: List[Dict[str, Any]]) -> SolveResult:
    constraints = canonicalize_constraints(
        constraints
    )
    feasible, model = _is_feasible(constraints)
    if not feasible:
        return SolveResult(
            status="UNSAT",
            unsat_core=_minimal_unsat_core(constraints),
            model_dates={},
        )

    dates = {
        name: from_day(day)
        for name, day in model.items()
        if name != ZERO
    }
    return SolveResult(status="SAT", unsat_core=[], model_dates=dates)
