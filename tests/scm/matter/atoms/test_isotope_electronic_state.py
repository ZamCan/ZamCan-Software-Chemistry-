import pytest

from scm.matter.atoms import Atom
from scm.matter.isotopes import Isotope


def test_isotope_identity_can_construct_atomic_electronic_state():
    isotope = Isotope.from_za(1, 2)
    atom = Atom.from_isotope(isotope)

    assert atom.atomic_number == 1
    assert atom.mass_number == 2
    assert atom.proton_count == 1
    assert atom.neutron_count == 1
    assert atom.electron_count == 1
    assert atom.isotope is not None
    assert atom.isotope.identity == (1, 2)
    assert atom.nucleus.identity == (1, 2)


def test_isotope_identity_preserves_ionic_electronic_state():
    isotope = Isotope.from_za(8, 18)
    atom = Atom.from_isotope(isotope, electron_count=10)

    assert atom.atomic_number == 8
    assert atom.mass_number == 18
    assert atom.neutron_count == 10
    assert atom.electron_count == 10
    assert atom.charge_number == -2


def test_atom_rejects_invalid_isotope_mass_number():
    with pytest.raises(ValueError, match="mass_number cannot be less"):
        Atom.create(8, mass_number=7)


def test_atom_without_isotope_has_no_nuclear_mass_identity():
    atom = Atom.create(1)

    assert atom.mass_number is None
    assert atom.neutron_count is None
    assert atom.isotope is None
    with pytest.raises(ValueError, match="nucleus is unavailable"):
        _ = atom.nucleus
