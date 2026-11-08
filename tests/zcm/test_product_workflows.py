import json
import subprocess
import sys

import pytest

from scm.core import Quantity
from zcm.sdk import ZCMClient


def test_calculator_uses_language_router_and_exact_reaction_amounts():
    client = ZCMClient()
    assert client.calculate("uzito wa moli H2O")["result"]["minimum"] == 18.01471
    mass = client.calculate("molar mass Ca(OH)2")
    assert mass["result"]["minimum"] == pytest.approx(74.09174)
    calcium = next(term for term in mass["contributions"] if term["element"] == "Ca")
    assert calcium["atomic_weight_uncertainty"]["absolute"] == 0.004
    assert calcium["references"][0]["source"] == "CIAAW, Standard Atomic Weights 2024"
    with pytest.raises(ValueError, match="No standard atomic weight"):
        client.calculate("molar mass Tc")
    assert client.calculate("balance equation H2 + O2 -> H2O")["reactant_coefficients"] == [2, 1]
    assert client.calculate("balance Ca(OH)2 + HCl -> CaCl2 + H2O")["product_coefficients"] == [1, 2]
    for equation in ("H2 + -> H2", "Xx2 -> Xx", "H2 + O2 -> H2O + H2O2"):
        with pytest.raises(ValueError):
            client.calculate(f"balance {equation}")
    result = client.stoichiometry("H2 + O2 -> H2O", {"H2": "0.3", "O2": "0.2"})
    assert result["limiting_reactants"] == ["H2"]
    assert result["produced"] == {"H2O": "3/10"}
    assert result["remaining"]["O2"] == "1/20"
    with pytest.raises(ValueError):
        client.stoichiometry("H2 + O2 -> H2O", {"H2": "-0.3", "O2": "0.2"})
    assert client.titrate(0.1, 25, 20, 2)["analyte_concentration_mol_l"] == pytest.approx(0.25)


def test_notebook_and_simulator_through_separate_cli_invocations(tmp_path):
    db = tmp_path / "notebook.db"

    def run(*args, ok=True):
        result = subprocess.run(
            [sys.executable, "-m", "zcm.cli", "--db", str(db), *args],
            capture_output=True,
            text=True,
        )
        if ok:
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)
        assert result.returncode == 2
        return result.stderr

    experiment = run("lab", "create", "Titration", "Measure replicate titres")["experiment_id"]
    assert run("lab", "list")[0]["id"] == experiment
    run("lab", "measure", experiment, "titre", "24", "mL", "--instrument", "B-1", "--uncertainty", "0.05")
    run("lab", "measure", experiment, "titre", "26", "mL")
    assert "finite" in run("lab", "measure", experiment, "titre", "nan", "mL", ok=False)
    run("lab", "measure", experiment, "titre", "0.025", "L")
    run("lab", "note", experiment, "Endpoint observed")
    run("lab", "dataset", experiment, "ds1", "v1", "Bench data", "lab-log-1")
    summary = run("lab", "summarize", experiment, "titre", "mL", "--save")
    assert summary["mean"] == 25
    assert summary["sample_standard_deviation"] == pytest.approx(2 ** 0.5)
    assert summary["measurement_sequences"] == [1, 2]
    run("titrate", "0.1", "25", "20", "--experiment", experiment)
    concentration = run("molarity", "25", "500", "--amount-unit", "mmol", "--experiment", experiment)
    assert concentration["result"] == {"value": 0.05}

    plan = {
        "vessels": {
            "stock": {"capacity_ul": 400, "volume_ul": 300},
            "sample": {"capacity_ul": 100, "volume_ul": 0},
        },
        "steps": [{"source": "stock", "destination": "sample", "volume_ul": 100}],
    }
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    simulation = run("simulate-transfers", str(path), "--experiment", experiment)
    assert simulation["final_volumes_ul"] == {"stock": 200, "sample": 100}
    plan["steps"].append(plan["steps"][0])
    path.write_text(json.dumps(plan), encoding="utf-8")
    assert "destination capacity" in run("simulate-transfers", str(path), "--experiment", experiment, ok=False)
    exported = run("lab", "export", experiment)
    assert exported["events"][-2]["payload"]["input"]["amount"]["unit"] == "mmol"
    assert [event["kind"] for event in exported["events"]] == [
        "measurement", "measurement", "measurement", "observation", "dataset",
        "calculation", "calculation", "calculation", "simulation",
    ]


def test_concentration_units_bounds_and_mass_interval():
    client = ZCMClient()
    assert client.chemistry.molarity(Quantity(25, "mmol"), Quantity(500, "mL")).to("mmol/L").value == 50
    assert client.dilute(Quantity(1000, "mmol/L"), Quantity(25, "mL"), Quantity(0.25, "L"))["result"] == {
        "value": 0.1,
    }
    salt = client.mass_molarity("NaCl", Quantity(5844, "mg"), Quantity(1, "L"))
    assert salt["result"]["minimum"] == pytest.approx(5.844 / salt["molar_mass"]["maximum"])
    assert salt["result"]["maximum"] == pytest.approx(5.844 / salt["molar_mass"]["minimum"])
    with pytest.raises(ValueError, match="Incompatible dimensions"):
        client.molarity(Quantity(5, "g"), Quantity(500, "mL"))
    for invalid_volume in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            client.molarity(Quantity(1, "mol"), Quantity(invalid_volume, "mL"))
    with pytest.raises(ValueError, match="at least"):
        client.dilute(Quantity(1, "mol/L"), Quantity(100, "mL"), Quantity(50, "mL"))
