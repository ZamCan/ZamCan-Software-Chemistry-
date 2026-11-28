import math
import pytest
from scm.practical_science import calculate, Conditions, ideal_gas_molar_volume_m3
from zcm.cli import scientific_operation

@pytest.mark.parametrize("name,inputs,expected", [
    ("density",dict(mass_kg=2,volume_m3=.001),2000),
    ("molarity",dict(amount_mol=.1,solution_volume_m3=.001),100),
    ("ph",dict(hydrogen_activity=1e-7),7),
    ("force",dict(mass_kg=2,acceleration_m_s2=3),6),
    ("kinetic_energy",dict(mass_kg=2,speed_m_s=3),9),
    ("radioactive_remaining",dict(initial_amount=100,elapsed_s=20,half_life_s=10),25),
    ("dilution_volume",dict(initial_concentration=2,initial_volume_m3=.001,final_concentration=1),.002),
    ("displacement",dict(initial_velocity_m_s=2,acceleration_m_s2=4,elapsed_s=3),24),
])
def test_formula(name,inputs,expected):
    result=scientific_operation("formula",dict(name=name,quantities=inputs))
    assert result["value"] == pytest.approx(expected)
    assert result["status"] == "calculated"
    assert result["assumptions"]

def test_missing_conditions():
    with pytest.raises(ValueError):
        ideal_gas_molar_volume_m3(Conditions(298.15))

def test_invalid_values():
    with pytest.raises(ValueError):
        calculate("density",mass_kg=1,volume_m3=0)
    with pytest.raises(ValueError):
        calculate("mass_fraction",solute_mass_kg=2,solution_mass_kg=1)
    with pytest.raises(ValueError):
        calculate("force",mass_kg=math.nan,acceleration_m_s2=1)

def test_catalog():
    assert len(scientific_operation("formula-catalog",{})) >= 39
    assert scientific_operation("constants",{})["avogadro"]["exact"]

def test_sheet_no_fabrication():
    result=scientific_operation("qualitative-sheet",dict(sample_id="A",observations=[],profile="necta_draft"))
    assert result["conclusion"] is None
    assert not result["official_format_verified"]
