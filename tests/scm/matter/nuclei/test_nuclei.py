from __future__ import annotations

import pytest

from scm.matter.nuclei import Nucleus


def test_nucleus_counts_define_mass_number():
    nucleus = Nucleus(proton_count=6, neutron_count=6)

    assert nucleus.atomic_number == 6
    assert nucleus.neutron_number == 6
    assert nucleus.mass_number == 12
    assert nucleus.nucleon_count == 12
    assert nucleus.identity == (6, 12)


def test_nucleus_can_be_constructed_from_z_and_a():
    nucleus = Nucleus.from_mass_number(6, 13)

    assert nucleus.proton_count == 6
    assert nucleus.neutron_count == 7
    assert nucleus.mass_number == 13


def test_nucleus_rejects_invalid_proton_count():
    with pytest.raises(ValueError):
        Nucleus(proton_count=0, neutron_count=0)

    with pytest.raises(ValueError):
        Nucleus(proton_count=119, neutron_count=0)


def test_nucleus_rejects_negative_neutrons():
    with pytest.raises(ValueError):
        Nucleus(proton_count=6, neutron_count=-1)


def test_mass_number_cannot_be_less_than_atomic_number():
    with pytest.raises(ValueError):
        Nucleus.from_mass_number(6, 5)
