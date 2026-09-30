from scm.matter.ions import Ion


def test_sodium_cation():
    ion = Ion(atomic_number=11, charge_number=1, symbol="Na")

    assert ion.proton_count == 11
    assert ion.electron_count == 10
    assert ion.is_cation
    assert not ion.is_anion
    assert ion.classification == "cation"
    assert ion.configuration.notation() == "1s2 2s2 2p6"


def test_chloride_anion():
    ion = Ion(atomic_number=17, charge_number=-1, symbol="Cl")

    assert ion.proton_count == 17
    assert ion.electron_count == 18
    assert ion.is_anion
    assert not ion.is_cation
    assert ion.classification == "anion"
    assert ion.configuration.notation() == "1s2 2s2 2p6 3s2 3p6"
