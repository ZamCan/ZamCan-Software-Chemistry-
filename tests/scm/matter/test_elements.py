from scm.matter.elements import Element


def test_element_derives_neutral_atom_electronic_structure():
    hydrogen = Element(1)

    assert hydrogen.proton_count == 1
    assert hydrogen.neutral_atom.is_neutral_atom
    assert hydrogen.electron_configuration.electron_count == 1
    assert hydrogen.electron_configuration.notation() == "1s1"
    assert hydrogen.valence_electron_count == 1


def test_element_electronic_structure_uses_atomic_identity():
    iron = Element(26)

    assert iron.neutral_atom.electron_count == 26
    assert iron.electron_configuration.electron_count == 26
    assert iron.valence_electron_count == 2


def test_element_exposes_modeled_ground_state_exception():
    chromium = Element(24)

    assert chromium.electron_configuration.electron_count == 24
    assert "4s1" in chromium.electron_configuration.notation()
    assert "3d5" in chromium.electron_configuration.notation()
