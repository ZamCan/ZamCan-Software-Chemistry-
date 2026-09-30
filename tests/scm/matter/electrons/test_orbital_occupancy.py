from __future__ import annotations

import pytest

from scm.matter.electrons import (
    ElectronOrbital,
    ElectronSpin,
    OrbitalElectron,
)


def test_electron_spin_quantum_numbers():
    assert ElectronSpin.UP.quantum_number == 0.5
    assert ElectronSpin.DOWN.quantum_number == -0.5


def test_orbital_electron_requires_valid_spin():
    electron = OrbitalElectron(ElectronSpin.UP)

    assert electron.spin is ElectronSpin.UP
    assert electron.spin_quantum_number == 0.5


def test_orbital_rejects_more_than_two_electrons():
    with pytest.raises(ValueError):
        ElectronOrbital(
            principal_level=2,
            subshell="p",
            magnetic_quantum_number=0,
            electron_count=3,
        )


def test_empty_orbital_has_no_electrons():
    orbital = ElectronOrbital(
        principal_level=2,
        subshell="p",
        magnetic_quantum_number=-1,
    )

    assert orbital.is_empty
    assert orbital.possible_spins == ()


def test_single_occupancy_has_one_spin_state():
    orbital = ElectronOrbital(
        principal_level=2,
        subshell="p",
        magnetic_quantum_number=-1,
        electron_count=1,
    )

    assert orbital.is_singly_occupied
    assert len(orbital.possible_spins) == 1
    assert orbital.possible_spins[0].spin is ElectronSpin.UP


def test_double_occupancy_has_opposite_spins():
    orbital = ElectronOrbital(
        principal_level=2,
        subshell="p",
        magnetic_quantum_number=0,
        electron_count=2,
    )

    assert orbital.is_doubly_occupied
    assert tuple(
        electron.spin
        for electron in orbital.possible_spins
    ) == (
        ElectronSpin.UP,
        ElectronSpin.DOWN,
    )


def test_double_occupancy_contains_two_distinct_spin_projections():
    orbital = ElectronOrbital(
        principal_level=1,
        subshell="s",
        magnetic_quantum_number=0,
        electron_count=2,
    )

    spin_values = {
        electron.spin_quantum_number
        for electron in orbital.possible_spins
    }

    assert spin_values == {0.5, -0.5}
