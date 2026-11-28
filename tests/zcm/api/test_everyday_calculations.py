import json

import pytest

from zcm.api import zcm
from zcm.cli import main


@pytest.mark.parametrize(("operation", "inputs", "expected"), [
    ("ph", {"activity": 0.000001}, 6),
    ("dilution", {"initial_l": 1, "initial_mol_l": 2, "final_l": 4}, 0.5),
    ("water-hardness", {"calcium_mg_l": 40.078, "magnesium_mg_l": 24.305}, 200.1738),
    ("electrical-energy", {"voltage_v": 2, "current_a": 3, "seconds": 4}, 24),
])
def test_everyday_command(tmp_path, capsys, operation, inputs, expected):
    path = tmp_path / "measurement.json"
    path.write_text(json.dumps({"operation": operation, "inputs": inputs}))
    main(["everyday", str(path)])
    record = json.loads(capsys.readouterr().out)
    assert record["result"]["value"] == pytest.approx(expected)
    assert record["inputs"] == inputs
    assert record["experimental_confirmation"] is False


def test_private_dispatch_rejected():
    with pytest.raises(AttributeError):
        zcm.execute("calculation", "__init__")


def test_boolean_measurement_rejected():
    with pytest.raises(ValueError):
        zcm.execute("everyday_chemistry", "reason", "ph", {"activity": True})
