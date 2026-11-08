import json
import subprocess
import sys

import pytest

from zcm.sdk import ZCMClient


@pytest.mark.parametrize(("evidence", "route", "expected"), [
    ({"amount": {"value": 25, "unit": "mmol"}, "final_volume": {"value": 500, "unit": "mL"}},
     "amount", 0.05),
    ({"formula": "Ca", "mass": {"value": 40.078, "unit": "g"}, "final_volume": {"value": 1, "unit": "L"}},
     "mass", 1),
    ({"stock": {"value": 1, "unit": "mol/L"}, "aliquot": {"value": 25, "unit": "mL"},
      "final_volume": {"value": 250, "unit": "mL"}}, "dilution", 0.1),
    ({"titrant_mol_l": 0.1, "titrant_ml": 25, "analyte_ml": 20, "ratio": 0.5}, "titration_ratio", 0.0625),
    ({"titrant_mol_l": 0.1, "titrant_ml": 25, "analyte_ml": 20, "titrant": "NaOH", "analyte": "H2SO4",
      "equation": "NaOH + H2SO4 -> Na2SO4 + H2O"}, "titration_equation", 0.0625),
])
def test_reasoning_routes(evidence, route, expected):
    result = ZCMClient().infer_concentration(evidence)
    assert result["status"] == "calculated"
    assert result["route"] == route
    assert result["candidates"][0]["missing"] == []
    calculation = result["calculation"]
    actual = (
        calculation["result"]["value"]
        if "result" in calculation else calculation["analyte_concentration_mol_l"]
    )
    assert actual == pytest.approx(expected)


def test_reasoning_requests_evidence_and_reports_conflict():
    infer = ZCMClient().infer_concentration
    partial = {"titrant_mol_l": 0.1, "titrant_ml": 25, "analyte_ml": 20}
    result = infer(partial)
    assert result["status"] == "needs_evidence"
    assert [candidate["missing"] for candidate in result["candidates"]] == [
        ["ratio"], ["equation", "titrant", "analyte"],
    ]
    assert "calculation" not in result
    assert infer({**partial, "ratio": 1, "equation": "HCl + NaOH -> NaCl + H2O"})[
        "status"
    ] == "conflicting_evidence"
    assert infer({"amount": {"value": 1, "unit": "g"}})["field"] == "amount"
    assert infer({"volum": 20})["unknown_fields"] == ["volum"]
    invalid = infer({"amount": {"value": 1, "unit": "mol"}, "final_volume": {"value": 0, "unit": "mL"}})
    assert invalid["status"] == "invalid_input"
    assert "calculation" not in invalid


def test_cli_persists_only_completed_reasoning(tmp_path):
    db = tmp_path / "reasoning.db"
    notebook = ZCMClient().open_notebook(db)
    experiment = notebook.create("Concentration", "Check inference").experiment_id
    amount = {"amount": {"value": 25, "unit": "mmol"}}

    def run(evidence):
        return json.loads(subprocess.check_output([
            sys.executable, "-m", "zcm.cli", "--db", str(db), "infer-concentration",
            json.dumps(evidence), "--experiment", experiment,
        ], text=True))

    assert run(amount)["status"] == "needs_evidence"
    assert notebook.export(experiment)["events"] == []
    result = run({**amount, "final_volume": {"value": 500, "unit": "mL"}})
    event, = notebook.export(experiment)["events"]
    assert event["sequence"] == result.pop("record_sequence")
    assert event["payload"] == result
