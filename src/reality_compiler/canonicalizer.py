def canonicalize_constraints(constraints):
    """
    Resolve explicit same_event relations deterministically.

    same_event constraints are used to build equivalence classes
    of event symbols. All remaining constraints are then rewritten
    to use one canonical event name.

    The same_event constraints themselves are removed before the
    feasibility solver runs.
    """

    parents = {}

    def find(item):
        parents.setdefault(
            item,
            item,
        )

        if parents[item] != item:
            parents[item] = find(
                parents[item]
            )

        return parents[item]

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a == root_b:
            return

        # Deterministic canonical name:
        # alphabetically smaller symbol wins.
        canonical = min(
            root_a,
            root_b,
        )

        other = max(
            root_a,
            root_b,
        )

        parents[other] = canonical

    # First pass:
    # collect all event symbols.
    for constraint in constraints:
        event = constraint.get(
            "event"
        )

        ref = constraint.get(
            "ref"
        )

        if event:
            find(event)

        if ref:
            find(ref)

    # Second pass:
    # process explicit semantic identity.
    for constraint in constraints:
        if constraint.get("kind") == "same_event":
            union(
                constraint["event"],
                constraint["ref"],
            )

    normalized = []

    # Third pass:
    # rewrite all normal constraints.
    for constraint in constraints:
        if constraint.get("kind") == "same_event":
            continue

        item = dict(
            constraint
        )

        event = item.get(
            "event"
        )

        if event:
            item["event"] = find(
                event
            )

        ref = item.get(
            "ref"
        )

        if ref:
            item["ref"] = find(
                ref
            )

        normalized.append(
            item
        )

    return normalized