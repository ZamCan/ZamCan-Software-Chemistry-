from __future__ import annotations

import pytest

from scm.matter.isotopes import Isotope


def test_carbon_12_identity():
    isotope = Isotope.from_za(6, 12)

    assert isotope.atomic_number == 6
    assert isotope.neutron_number == 6
    assert isotope.mass_number == 12
    assert isotope.identity == (6, 12)


def test_carbon_13_identity():
    isotope = Isotope.from_za(6, 13)

    assert isotope.atomic_number == 6
    assert isotope.neutron_number == 7
    assert isotope.mass_number == 13
    assert isotope.identity == (6, 13)


def test_zn_constructor():
    isotope = Isotope.from_zn(8, 10)

    assert isotope.atomic_number == 8
    assert isotope.neutron_number == 10
    assert isotope.mass_number == 18


def test_same_element():
    carbon_12 = Isotope.from_za(6, 12)
    carbon_13 = Isotope.from_za(6, 13)
    nitrogen_13 = Isotope.from_za(7, 13)

    assert carbon_12.same_element(carbon_13)
    assert not carbon_12.same_element(nitrogen_13)


def test_same_isotope():
    carbon_12_a = Isotope.from_za(6, 12)
    carbon_12_b = Isotope.from_zn(6, 6)
    carbon_13 = Isotope.from_za(6, 13)

    assert carbon_12_a.same_isotope(carbon_12_b)
    assert not carbon_12_a.same_isotope(carbon_13)


def test_isotope_requires_nucleus():
    with pytest.raises(TypeError):
        Isotope(nucleus="not-a-nucleus")  # type: ignore[arg-type]
