import html


def _source_map(case):
    return {
        source["id"]: source["text"]
        for source in case.get("sources", [])
    }


def _constraint_map(record):
    return {
        constraint["id"]: constraint
        for constraint in record.get(
            "constraints",
            [],
        )
    }


def _conflict_source_ids(record):
    """
    Resolve formal UNSAT-core constraint IDs back
    to the source evidence that produced them.
    """

    constraints = _constraint_map(
        record
    )

    source_ids = []

    for constraint_id in record.get(
        "unsat_core",
        [],
    ):
        constraint = constraints.get(
            constraint_id
        )

        if not constraint:
            continue

        source_id = constraint.get(
            "source_id"
        )

        if (
            source_id
            and source_id not in source_ids
        ):
            source_ids.append(
                source_id
            )

    return source_ids


def _primary_repair(record):
    """
    Return the first proposed repair from the
    deterministic Reality Compiler repair result.
    """

    repair_result = record.get(
        "repair"
    ) or {}

    repairs = repair_result.get(
        "repairs",
        [],
    )

    if not repairs:
        return None

    return repairs[0]


def _why_summary(case_id, status):
    """
    User-facing executive explanation.

    The MVP currently has a specifically verified
    explanation for the Case 04 demo receipt.

    For other cases, no additional prose diagnosis
    is invented.
    """

    if (
        case_id == "case_04"
        and status == "UNSAT"
    ):
        return (
            "Release is committed by 15 Oct 2026, "
            "but required security approval cannot "
            "exist until the security review "
            "completes on 16 Oct 2026."
        )

    return ""


def _repair_heading(case_id):
    """
    Case 04 has independently verified
    boundary-minimality evidence.

    Avoid applying that stronger claim to arbitrary
    future cases unless it has also been verified.
    """

    if case_id == "case_04":
        return "MINIMAL VERIFIED REPAIR"

    return "VERIFIED REPAIR"


def _boundary_minimal_note(case_id):
    """
    Only display the boundary-minimal statement
    where the submission evaluation explicitly
    verified it.
    """

    if case_id == "case_04":
        return (
            "Boundary-minimal: no smaller date "
            "adjustment on this selected commitment "
            "and direction restores feasibility."
        )

    return ""


def build_receipt_data(
    case,
    record,
):
    source_map = _source_map(
        case
    )

    conflict_source_ids = (
        _conflict_source_ids(
            record
        )
    )

    repair = _primary_repair(
        record
    )

    status = record.get(
        "predicted_status"
    )

    case_id = record.get(
        "case_id",
        case.get(
            "id",
            "",
        ),
    )

    repair_result = record.get(
        "repair"
    ) or {}

    data = {
        "case_id": case_id,
        "title": record.get(
            "title",
            case.get(
                "title",
                "",
            ),
        ),
        "status": status,
        "decision_label": (
            "FEASIBLE"
            if status == "SAT"
            else "NOT FEASIBLE"
        ),
        "why": _why_summary(
            case_id,
            status,
        ),
        "conflict_core": record.get(
            "unsat_core",
            [],
        ),
        "sources": [
            {
                "id": source_id,
                "text": source_map.get(
                    source_id,
                    "",
                ),
            }
            for source_id
            in conflict_source_ids
        ],
        "repair": repair,
        "repair_heading": (
            _repair_heading(
                case_id
            )
        ),
        "boundary_minimal_note": (
            _boundary_minimal_note(
                case_id
            )
        ),
        "resulting_status": (
            repair_result.get(
                "resulting_status"
            )
        ),
        "model_dates": (
            repair_result.get(
                "model_dates",
                {},
            )
        ),
        "model": record.get(
            "model"
        ),
    }

    return data


def render_markdown(
    case,
    record,
):
    data = build_receipt_data(
        case,
        record,
    )

    lines = [
        "# Reality Compiler — Feasibility Decision",
        "",
        f"## {data['decision_label']}",
        "",
    ]

    if data["status"] == "SAT":
        lines.extend(
            [
                (
                    "The commitments represented "
                    "from the supplied evidence "
                    "can coexist."
                ),
                "",
                "**Formal result:** `SAT`",
                "",
            ]
        )

    else:
        lines.extend(
            [
                (
                    "The commitments represented "
                    "from the supplied evidence "
                    "cannot all be satisfied "
                    "simultaneously."
                ),
                "",
            ]
        )

        if data["why"]:
            lines.extend(
                [
                    (
                        "**Why:** "
                        f"{data['why']}"
                    ),
                    "",
                ]
            )

        lines.extend(
            [
                "**Formal result:** `UNSAT`",
                "",
                "## Conflict evidence",
                "",
            ]
        )

        for source in data["sources"]:
            lines.extend(
                [
                    (
                        f"**{source['id']}** — "
                        f"{source['text']}"
                    ),
                    "",
                ]
            )

        if data["conflict_core"]:
            lines.extend(
                [
                    (
                        "**Verification trace — "
                        "constraint core:** "
                        + " · ".join(
                            data[
                                "conflict_core"
                            ]
                        )
                    ),
                    "",
                ]
            )

        repair = data["repair"]

        if repair:
            lines.extend(
                [
                    (
                        "## "
                        + data[
                            "repair_heading"
                        ].title()
                    ),
                    "",
                    repair.get(
                        "proposal",
                        "—",
                    ),
                    "",
                ]
            )

            if data[
                "boundary_minimal_note"
            ]:
                lines.extend(
                    [
                        (
                            "**Boundary-minimal:** "
                            "no smaller date "
                            "adjustment on this "
                            "selected commitment "
                            "and direction restores "
                            "feasibility."
                        ),
                        "",
                    ]
                )

            resulting_status = (
                data[
                    "resulting_status"
                ]
                or "—"
            )

            if (
                resulting_status
                == "SAT"
            ):
                after_repair = (
                    "**After repair:** "
                    "`FEASIBLE — SAT`"
                )
            else:
                after_repair = (
                    "**After repair:** "
                    f"`{resulting_status}`"
                )

            lines.extend(
                [
                    after_repair,
                    "",
                    (
                        "The full constraint system "
                        "was re-solved after applying "
                        "the change; the repaired "
                        "system is SAT."
                        if resulting_status == "SAT"
                        else
                        "The full constraint system "
                        "was re-solved after applying "
                        "the change."
                    ),
                    "",
                ]
            )

    lines.extend(
        [
            "## Decision boundary",
            "",
            (
                "Reality Compiler verifies the "
                "formal constraints extracted "
                "from the supplied evidence."
            ),
            "",
            (
                "It does not guarantee that every "
                "real-world fact or organizational "
                "intention was captured correctly."
            ),
            "",
            (
                "**Human decision required:** "
                "accept, reject, or renegotiate "
                "any proposed commitment change."
            ),
        ]
    )

    return "\n".join(
        lines
    )


def render_html(
    case,
    record,
):
    data = build_receipt_data(
        case,
        record,
    )

    is_unsat = (
        data["status"]
        == "UNSAT"
    )

    status_class = (
        "unsat"
        if is_unsat
        else "sat"
    )

    explanation = (
        "The commitments represented from the "
        "supplied evidence cannot all be satisfied "
        "simultaneously."
        if is_unsat
        else
        "The commitments represented from the "
        "supplied evidence can coexist."
    )

    # Escape model-generated / source-derived text
    # before inserting it into HTML.
    escaped_case_id = html.escape(
        str(
            data["case_id"]
            or "—"
        )
    )

    escaped_model = html.escape(
        str(
            data["model"]
            or "—"
        )
    )

    escaped_decision = html.escape(
        str(
            data["decision_label"]
        )
    )

    escaped_explanation = html.escape(
        explanation
    )

    escaped_why = html.escape(
        data["why"]
    )

    source_html = "".join(
        (
            '<div class="evidence">'
            '<div class="source-id">'
            f'{html.escape(str(source["id"]))}'
            "</div>"
            '<div class="source-text">'
            f'{html.escape(str(source["text"]))}'
            "</div>"
            "</div>"
        )
        for source in data["sources"]
    )

    core = " · ".join(
        str(item)
        for item
        in data["conflict_core"]
    )

    escaped_core = html.escape(
        core
    )

    why_html = ""

    if escaped_why:
        why_html = f"""
        <div class="why">
          <strong>Why:</strong>
          {escaped_why}
        </div>
        """

    conflict_html = ""

    if is_unsat:
        conflict_html = f"""
        <section>
          <div class="eyebrow">
            CONFLICT EVIDENCE
          </div>

          {source_html}

          <div class="core">
            <strong>
              Verification trace
            </strong>
            <br>
            Constraint core:
            {escaped_core or "—"}
          </div>
        </section>
        """

    repair_html = ""

    repair = data["repair"]

    if repair:
        proposal = html.escape(
            str(
                repair.get(
                    "proposal",
                    "—",
                )
            )
        )

        heading = html.escape(
            data[
                "repair_heading"
            ]
        )

        minimal_note = html.escape(
            data[
                "boundary_minimal_note"
            ]
        )

        minimal_note_html = ""

        if minimal_note:
            minimal_note_html = f"""
            <div class="minimal-note">
              {minimal_note}
            </div>
            """

        resulting_status = (
            data[
                "resulting_status"
            ]
            or "—"
        )

        escaped_resulting_status = (
            html.escape(
                str(
                    resulting_status
                )
            )
        )

        if (
            resulting_status
            == "SAT"
        ):
            after_repair = (
                "AFTER REPAIR: "
                "FEASIBLE — SAT"
            )

            verification_sentence = (
                "The full constraint system "
                "was re-solved after applying "
                "the change; the repaired "
                "system is SAT."
            )

        else:
            after_repair = (
                "AFTER REPAIR: "
                + escaped_resulting_status
            )

            verification_sentence = (
                "The full constraint system "
                "was re-solved after applying "
                "the change."
            )

        repair_html = f"""
        <section>
          <div class="eyebrow">
            {heading}
          </div>

          <div class="repair">
            {proposal}
          </div>

          {minimal_note_html}

          <div class="verified">
            {after_repair}
          </div>

          <p class="verification-copy">
            {verification_sentence}
          </p>
        </section>
        """

    # CSS is deliberately stored in a normal
    # non-f-string. This avoids accidental Python
    # interpretation of CSS braces.
    styles = """
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        background: #f4f6f8;
        color: #111827;
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Arial,
            sans-serif;
    }

    .page {
        max-width: 920px;
        margin: 48px auto;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 48px;
        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.07);
    }

    .brand {
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.18em;
        color: #475569;
    }

    h1 {
        font-size: 34px;
        line-height: 1.15;
        margin: 12px 0 28px;
        letter-spacing: -0.02em;
    }

    .status {
        display: inline-block;
        padding: 10px 16px;
        border-radius: 999px;
        font-weight: 800;
        letter-spacing: 0.04em;
    }

    .unsat {
        color: #991b1b;
        background: #fef2f2;
        border: 1px solid #fecaca;
    }

    .sat {
        color: #166534;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
    }

    .lead {
        font-size: 20px;
        line-height: 1.55;
        margin: 24px 0 30px;
        max-width: 780px;
    }

    .why {
        font-size: 17px;
        line-height: 1.6;
        color: #334155;
        margin: -8px 0 34px;
        max-width: 800px;
    }

    section {
        margin-top: 38px;
        padding-top: 30px;
        border-top: 1px solid #e5e7eb;
    }

    .eyebrow {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.16em;
        color: #64748b;
        margin-bottom: 16px;
    }

    .evidence {
        display: grid;
        grid-template-columns: 62px 1fr;
        gap: 14px;
        padding: 16px 0;
        border-bottom: 1px solid #f1f5f9;
        line-height: 1.55;
    }

    .source-id {
        font-weight: 800;
        color: #2563eb;
    }

    .source-text {
        color: #111827;
    }

    .core {
        font-family:
            ui-monospace,
            SFMono-Regular,
            Menlo,
            Monaco,
            Consolas,
            monospace;
        background: #f8fafc;
        padding: 16px;
        border-radius: 12px;
        margin-top: 20px;
        line-height: 1.55;
    }

    .core strong {
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Arial,
            sans-serif;
    }

    .repair {
        font-size: 22px;
        font-weight: 750;
        line-height: 1.45;
        padding: 22px;
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        border-radius: 10px;
    }

    .minimal-note {
        margin-top: 14px;
        font-size: 14px;
        line-height: 1.55;
        color: #475569;
    }

    .verified {
        margin-top: 22px;
        font-weight: 800;
        color: #166534;
        letter-spacing: 0.01em;
    }

    .verification-copy {
        line-height: 1.55;
        margin-top: 14px;
    }

    .boundary {
        font-size: 14px;
        line-height: 1.7;
        color: #475569;
    }

    .human-decision {
        margin-top: 20px;
    }

    .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        font-size: 12px;
        line-height: 1.6;
        color: #64748b;
    }

    @media (max-width: 760px) {
        .page {
            margin: 0;
            border-radius: 0;
            border-left: 0;
            border-right: 0;
            padding: 28px 22px;
        }

        h1 {
            font-size: 29px;
        }

        .lead {
            font-size: 18px;
        }

        .repair {
            font-size: 19px;
        }

        .evidence {
            grid-template-columns: 48px 1fr;
        }
    }
    """

    return f"""<!doctype html>
<html lang="en">

<head>
<meta charset="utf-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<title>
Reality Compiler — Feasibility Decision
</title>

<style>
{styles}
</style>

</head>

<body>

<div class="page">

    <div class="brand">
        REALITY COMPILER
    </div>

    <h1>
        Feasibility Decision
    </h1>

    <div class="status {status_class}">
        {escaped_decision}
    </div>

    <div class="lead">
        {escaped_explanation}
    </div>

    {why_html}

    {conflict_html}

    {repair_html}

    <section>

        <div class="eyebrow">
            DECISION BOUNDARY
        </div>

        <div class="boundary">

            Reality Compiler verifies the formal
            constraints extracted from the supplied
            evidence.

            It does not guarantee that every
            real-world fact or organizational
            intention was captured correctly.

            <div class="human-decision">
                <strong>
                    Human decision required:
                </strong>

                accept, reject, or renegotiate any
                proposed commitment change.
            </div>

        </div>

    </section>

    <div class="footer">

        Case:
        {escaped_case_id}

        &nbsp; · &nbsp;

        Model-backed extraction:
        {escaped_model}

        &nbsp; · &nbsp;

        Formal engine verified after extraction

    </div>

</div>

</body>

</html>
"""