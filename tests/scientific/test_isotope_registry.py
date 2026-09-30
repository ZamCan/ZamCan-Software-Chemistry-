import pytest

from knowledge.isotopes import all_isotopes, get_isotope
from knowledge.isotopes.registry import register_isotope
from knowledge.isotopes.base import IsotopeRecord
from scm.matter.isotopes import Isotope
from scm.matter.nuclei import Nucleus


def test_hydrogen_isotopes_are_registered():
    isotopes = all_isotopes()

    assert len(isotopes) == 3
    assert {isotope.identity for isotope in isotopes} == {
        (1, 1),
        (1, 2),
        (1, 3),
    }


def test_isotope_can_be_found_by_name():
    assert get_isotope("protium").identity == (1, 1)
    assert get_isotope("deuterium").identity == (1, 2)
    assert get_isotope("tritium").identity == (1, 3)


def test_isotope_can_be_found_by_symbol():
    assert get_isotope("¹H").identity == (1, 1)
    assert get_isotope("²H").identity == (1, 2)
    assert get_isotope("³H").identity == (1, 3)


def test_isotope_can_be_found_by_identity():
    assert get_isotope((1, 1)).name == "Protium"
    assert get_isotope((1, 2)).name == "Deuterium"
    assert get_isotope((1, 3)).name == "Tritium"


def test_unknown_isotope_is_rejected():
    with pytest.raises(KeyError):
        get_isotope((1, 999))


def test_duplicate_identity_is_rejected():
    duplicate = IsotopeRecord(
        isotope=Isotope(Nucleus(1, 0)),
        name="Another Protium",
        symbol="X-H",
    )

    with pytest.raises(ValueError):
        register_isotope(duplicate)
