from scm.matter.atoms import build_atom, neutral_atom


def test_neutral_hydrogen_is_derived_from_atomic_number():
    atom = neutral_atom(1, symbol="H")

    assert atom.electron_count == 1
    assert atom.charge_number == 0
    assert atom.notation == "1s1"


def test_sodium_configuration_is_computed():
    atom = neutral_atom(11, symbol="Na")

    assert atom.electron_count == 11
    assert atom.notation == "1s2 2s2 2p6 3s1"


def test_chromium_known_ground_state_exception():
    atom = neutral_atom(24, symbol="Cr")

    assert atom.electron_count == 24
    assert atom.notation == "1s2 2s2 2p6 3s2 3p6 4s1 3d5"


def test_atomic_identity_determines_neutral_electron_count():
    atom = build_atom(17)

    assert atom.electron_count == 17
    assert atom.charge_number == 0
