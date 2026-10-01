from zcm.chemistry.molar_mass import molar_mass_workspace


def test_molar_mass_workspace_uses_scm_engine():
    result = molar_mass_workspace.calculate("H2O")
    assert result.species.formula == "H2O"
    assert result.molar_mass.minimum.to("g/mol").value == 18.01468
    assert result.molar_mass.maximum.to("g/mol").value == 18.01622
