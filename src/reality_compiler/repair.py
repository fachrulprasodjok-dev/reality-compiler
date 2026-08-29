from itertools import combinations
from typing import Dict, List, Any
from .solver import solve

def find_minimal_relaxation(constraints: List[Dict[str, Any]], core_ids: List[str]):
    by_id = {c["id"]: c for c in constraints}
    editable = [cid for cid in core_ids if by_id[cid].get("editable", False)]

    for k in range(1, len(editable) + 1):
        for relaxed in combinations(editable, k):
            remaining = [c for c in constraints if c["id"] not in relaxed]
            result = solve(remaining)
            if result.status == "SAT":
                repairs = []
                for cid in relaxed:
                    c = by_id[cid]
                    item = {
                        "relax_constraint_id": cid,
                        "source_id": c.get("source_id"),
                        "description": c.get("description", ""),
                    }
                    if c["kind"] == "deadline":
                        event = c["event"]
                        item["proposal"] = (
                            f"Move {event} deadline from {c['date']} "
                            f"to at least {result.model_dates.get(event)}"
                        )
                    else:
                        item["proposal"] = "Relax or renegotiate this commitment."
                    repairs.append(item)
                return {
                    "relaxation_count": k,
                    "repairs": repairs,
                    "resulting_status": result.status,
                    "model_dates": result.model_dates,
                }
    return None
