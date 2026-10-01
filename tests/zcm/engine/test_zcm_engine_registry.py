from zcm.engine import zcm_registry


def test_zcm_registry_contains_common_modules():
    names = {
        module.name
        for module in zcm_registry.all()
    }

    assert names == {
        "elements",
        "calculator",
        "reactions",
        "molar_mass",
    }


def test_zcm_registry_finds_periodic_table():
    modules = zcm_registry.find_capability("periodic_table")

    assert len(modules) == 1
    assert modules[0].name == "elements"


def test_zcm_registry_finds_calculation():
    modules = zcm_registry.find_capability("calculation")

    assert len(modules) == 1
    assert modules[0].name == "calculator"


def test_zcm_registry_finds_reaction_balancing():
    modules = zcm_registry.find_capability(
        "equation_balancing"
    )

    assert len(modules) == 1
    assert modules[0].name == "reactions"
