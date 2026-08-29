ALLOWED_CONSTRAINT_KINDS = {
    "deadline",
    "fixed_date",
    "earliest",
    "after_days",
    "before_or_same",
}


def validate_constraint(constraint):
    required = {
        "id",
        "kind",
        "event",
        "source_id",
        "description",
    }

    missing = required - set(constraint.keys())

    if missing:
        raise ValueError(
            f"Missing required fields: {sorted(missing)}"
        )

    if constraint["kind"] not in ALLOWED_CONSTRAINT_KINDS:
        raise ValueError(
            f"Unsupported constraint kind: {constraint['kind']}"
        )

    kind = constraint["kind"]

    if kind in {"deadline", "fixed_date", "earliest"}:
        if "date" not in constraint:
            raise ValueError(
                f"{kind} constraint requires 'date'"
            )

    if kind == "after_days":
        if "ref" not in constraint:
            raise ValueError(
                "after_days constraint requires 'ref'"
            )

        if "days" not in constraint:
            raise ValueError(
                "after_days constraint requires 'days'"
            )

    if kind == "before_or_same":
        if "ref" not in constraint:
            raise ValueError(
                "before_or_same constraint requires 'ref'"
            )

    return True


def validate_constraints(constraints):
    if not isinstance(constraints, list):
        raise ValueError("Constraints must be a list")

    seen_ids = set()

    for constraint in constraints:
        validate_constraint(constraint)

        cid = constraint["id"]

        if cid in seen_ids:
            raise ValueError(
                f"Duplicate constraint id: {cid}"
            )

        seen_ids.add(cid)

    return True