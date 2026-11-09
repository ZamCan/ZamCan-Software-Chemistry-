"""Render an offline, printable laboratory notebook snapshot."""
from html import escape


_STYLE = """
:root { color-scheme: light; font-family: system-ui, sans-serif; color: #182b38; }
body { max-width: 62rem; margin: auto; padding: 2rem 1.25rem; }
header { border-top: .3rem solid #166361; padding-top: 1rem; }
h1 { margin: .35rem 0; font-size: 2rem; }
h2 { margin-top: 1.8rem; font-size: 1.25rem; }
h3 { font-size: 1rem; }
p { white-space: pre-wrap; overflow-wrap: anywhere; }
.meta { color: #465c66; font-size: .875rem; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; text-align: left; font-size: .9rem; }
th, td { padding: .45rem; border-bottom: 1px solid #cbd7db; overflow-wrap: anywhere; }
thead { background: #eaf3f2; }
article { border: 1px solid #cbd7db; margin: .75rem 0; padding: .75rem; }
dl { display: grid; grid-template-columns: minmax(7rem, 1fr) 2fr; gap: .3rem .75rem; }
dt { font-weight: 600; overflow-wrap: anywhere; }
dd { margin: 0; min-width: 0; white-space: pre-wrap; overflow-wrap: anywhere; }
dd dl { margin: 0 0 .5rem; }
ul { margin: 0; padding-left: 1.1rem; }
@media screen and (max-width: 35rem) {
  dl { grid-template-columns: 1fr; }
  dd { margin-bottom: .35rem; }
}
a { color: #125956; }
@media print {
  @page { margin: 15mm; }
  body { max-width: none; margin: 0; padding: 0; }
  h2, h3 { break-after: avoid; }
  tr { break-inside: avoid; }
  thead { display: table-header-group; }
  .table-wrap { overflow: visible; }
}
"""


def _text(value):
    return escape("—" if value is None or value == "" else str(value))


def _label(value):
    return str(value).replace("_", " ")


def _record_link(sequence):
    return f'<a href="#record-{sequence}">#{sequence}</a>'


def _table(title, columns, records):
    if not records:
        return ""
    head = "".join(f'<th scope="col">{escape(label)}</th>' for label, _ in columns)
    rows = []
    for event in records:
        sequence = int(event["sequence"])
        cells = "".join(f'<td>{_text(event["payload"].get(key))}</td>' for _, key in columns)
        rows.append(f'<tr id="record-{sequence}"><th scope="row">#{sequence}</th>{cells}</tr>')
    return (
        f'<section><h2>{escape(title)}</h2><div class="table-wrap"><table>'
        f'<thead><tr><th scope="col">Record</th>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></section>'
    )


def _details(value):
    if isinstance(value, dict) and value:
        items = "".join(
            f"<dt>{_text(_label(key))}</dt><dd>{_details(item)}</dd>"
            for key, item in value.items()
        )
        return f"<dl>{items}</dl>"
    if isinstance(value, list) and value:
        return "<ul>" + "".join(f"<li>{_details(item)}</li>" for item in value) + "</ul>"
    if value in ({}, []):
        return "—"
    return _text(value)


def _analysis(event, source_sequences):
    payload = event["payload"]
    sequence = int(event["sequence"])
    method = payload.get("method") or event["kind"]
    status = payload.get("status")
    # Notebook exports carry links only for records with a matching ID in this snapshot.
    references = [
        *payload.get("measurement_sequences", []),
        *(row.get("record_sequence") for row in payload.get("observations", [])),
    ] if event["kind"] == "salt_analysis" or method == "replicate_summary" else []
    links = ", ".join(
        _record_link(ref) for ref in dict.fromkeys(references)
        if type(ref) is int and ref in source_sequences
    )
    evidence = f'<p>Source records {links}</p>' if links else ""
    formula = f'<p>Formula hypothesis <strong>{_text(payload["formula"])}</strong></p>' if (
        event["kind"] == "salt_analysis" and payload.get("formula")
    ) else ""
    data = _details({key: value for key, value in payload.items() if key not in {"method", "status"}})
    status_label = f' · {_text(_label(status))}' if isinstance(status, str) else ""
    return (
        f'<article id="record-{sequence}"><h3>#{sequence} · {_text(_label(method))}'
        f'{status_label}</h3>{formula}{evidence}{data}</article>'
    )


def render_practical_sheet(snapshot: dict) -> str:
    """Render a complete HTML document from a LabNotebook.export snapshot."""
    experiment = snapshot["experiment"]
    events = snapshot["events"]
    tables = (
        ("measurement", "Measurements", (
            ("Quantity", "quantity"), ("Value", "value"), ("Unit", "unit"),
            ("Instrument", "instrument_id"), ("Uncertainty", "uncertainty"),
        )),
        ("ion_observation", "Qualitative observations", (
            ("Sample", "sample"), ("Test", "test"), ("Outcome", "observation"),
        )),
        ("observation", "Observations", (("Notes", "text"),)),
        ("conclusion", "Conclusions", (("Notes", "text"),)),
        ("dataset", "Data sources", (
            ("Identifier", "dataset_id"), ("Version", "version"), ("Title", "title"),
            ("Source", "source"), ("License", "license"), ("Checksum", "checksum"),
            ("Retrieved", "retrieved_at"),
        )),
    )
    source_sequences = {
        event["sequence"] for event in events if event["kind"] in {"measurement", "ion_observation"}
    }
    sections = []
    for kind, heading, columns in tables:
        sections.append(_table(heading, columns, [event for event in events if event["kind"] == kind]))
    table_kinds = {kind for kind, _, _ in tables}
    analyses = "".join(_analysis(event, source_sequences) for event in events if event["kind"] not in table_kinds)
    if analyses:
        sections.append(f'<section><h2>Calculations and analyses</h2>{analyses}</section>')
    if not events:
        sections.append("<p>No records have been added to this experiment.</p>")

    title = _text(experiment["title"])
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · ZCM practical sheet</title><style>{_STYLE}</style></head>
<body><header><div class="meta">ZCM LABORATORY PRACTICAL</div><h1>{title}</h1>
<p class="meta">Experiment {_text(experiment["id"])} · Created {_text(experiment["created_at"])}</p>
</header><main><section><h2>Objective</h2><p>{_text(experiment["objective"])}</p></section>
{"".join(sections)}</main></body>
</html>
"""
