import pytest

from scm.matter.ions import Ion
from scm.matter.isotopes import Isotope


def test_isotope_identity_is_preserved_in_ion():
    isotope = Isotope.from_za(17, 37)
    ion = Ion.from_isotope(isotope, 1)

    assert ion.atomic_number == 17
    assert ion.mass_number == 37
    assert ion.proton_count == 17
    assert ion.neutron_count == 20
    assert ion.electron_count == 16
    assert ion.charge_number == 1
    assert ion.isotope is not None
    assert ion.isotope.identity == (17, 37)
    assert ion.nucleus.identity == (17, 37)


def test_ion_charge_and_electron_state_remain_consistent_with_isotope():
    ion = Ion.create(8, -2, mass_number=18)

    assert ion.electron_count == 10
    assert ion.neutron_count == 10
    assert ion.atom_state.mass_number == 18
    assert ion.atom_state.electron_count == 10


def test_ion_rejects_invalid_mass_number():
    with pytest.raises(ValueError, match="mass_number cannot be less"):
        Ion.create(8, -2, mass_number=7)
