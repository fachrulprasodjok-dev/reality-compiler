def apply_repair_policy(constraints):
    """
    Adds repairability metadata separately from factual extraction.

    For the MVP:
    - deadlines are candidate commitments that may be renegotiated
    - all other constraints remain locked unless explicitly marked editable

    This does NOT change the factual meaning of any constraint.
    """

    annotated = []

    for constraint in constraints:
        item = dict(constraint)

        if "editable" not in item:
            item["editable"] = (
                item["kind"] == "deadline"
            )

        annotated.append(item)

    return annotated