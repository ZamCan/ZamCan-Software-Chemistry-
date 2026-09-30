from zcm.api import zcm


def test_zcm_exposes_common_modules():
    names = {
        module["name"]
        for module in zcm.modules()
    }

    assert names == {
        "elements",
        "calculator",
        "reactions",
    }


def test_zcm_exposes_capabilities():
    capabilities = zcm.capabilities()

    assert "periodic_table" in capabilities
    assert "calculation" in capabilities
    assert "equation_balancing" in capabilities


def test_zcm_dispatches_element_lookup():
    hydrogen = zcm.execute(
        "element_lookup",
        "get",
        "H",
    )

    assert hydrogen.atomic_number == 1
    assert hydrogen.symbol == "H"


def test_zcm_dispatches_reaction_balancing():
    result = zcm.execute(
        "equation_balancing",
        "balance",
        ["H2", "O2"],
        ["H2O"],
    )

    assert result.formatted() == "2H2 + O2 → 2H2O"
