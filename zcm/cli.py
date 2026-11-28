from __future__ import annotations
import argparse
import json
from dataclasses import asdict
from scm import practical_science as practical
from scm.chemistry import assign_oxidation_states, gibbs_free_energy
from scm.scientific_validation import benchmark, conservation_residual
from scm.evidence_reasoning import Evidence, compare_properties

def scientific_operation(operation, payload):
    """Shared entry point for CLI and future application adapters."""
    if operation == "formula":
        return practical.calculate(payload["name"], **payload["quantities"])
    if operation == "formula-catalog":
        return practical.formula_catalog()
    if operation == "constants":
        return practical.constants_catalog()
    if operation == "measurements":
        return practical.measurement_summary(payload["values"])
    if operation == "negligibility":
        return practical.negligibility(**payload)
    if operation == "qualitative-sheet":
        return practical.qualitative_sheet(payload["sample_id"],
            [practical.Observation(**row) for row in payload["observations"]],
            payload.get("profile", "general"))
    if operation == "benchmark":
        return asdict(benchmark(**payload))
    if operation == "conservation":
        result = conservation_residual(**payload)
        return {"status": "conserved" if not result["atoms"] and not result["charge"] else "rejected",
                "residual": result, "limitation": "Conservation is not proof of feasibility."}
    if operation == "compare-properties":
        records = [{**payload[k], "evidence": Evidence(**payload[k]["evidence"])} for k in ("a", "b")]
        return compare_properties(*records)
    raise ValueError("Unsupported operation")

def main(argv=None):
    p=argparse.ArgumentParser(prog="zcm")
    sub=p.add_subparsers(dest="command",required=True)
    ox=sub.add_parser("oxidation"); ox.add_argument("formula"); ox.add_argument("--charge",type=int,default=0)
    dg=sub.add_parser("gibbs"); dg.add_argument("delta_h",type=float); dg.add_argument("delta_s",type=float); dg.add_argument("temperature",type=float)
    for name in ("benchmark", "conservation", "compare-properties", "formula", "formula-catalog", "constants", "measurements", "negligibility", "qualitative-sheet"):
        cmd=sub.add_parser(name)
        cmd.add_argument("json_file", help="Path to JSON input")
    a=p.parse_args(argv)
    if a.command=="oxidation":
        print(assign_oxidation_states(a.formula,a.charge))
    elif a.command=="gibbs":
        print(gibbs_free_energy(a.delta_h,a.delta_s,a.temperature))
    else:
        try:
            with open(a.json_file, encoding="utf-8") as f:
                payload=json.load(f)
            print(json.dumps(scientific_operation(a.command,payload),allow_nan=False))
        except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
            p.error(str(exc))

if __name__=="__main__": main()
