import pytest

from scm.matter.electrons import (
    ElectronOrbital,
    ElectronSubshell,
    SubshellOccupancy,
    define_subshell,
)


@pytest.mark.parametrize(
    ("n", "subshell"),
    [
        (1, "s"),
        (2, "p"),
        (3, "d"),
        (4, "f"),
    ],
)
def test_occupancy_uses_canonical_definition(n, subshell):
    occupancy = SubshellOccupancy.from_electron_count(
        n,
        subshell,
        0,
    )

    assert occupancy.definition == define_subshell(
        n,
        subshell,
    )


@pytest.mark.parametrize(
    ("n", "subshell", "capacity"),
    [
        (1, "s", 2),
        (2, "p", 6),
        (3, "d", 10),
        (4, "f", 14),
    ],
)
def test_occupancy_capacity_matches_definition(
    n,
    subshell,
    capacity,
):
    occupancy = SubshellOccupancy.from_electron_count(
        n,
        subshell,
        capacity,
    )

    assert occupancy.capacity == capacity
    assert occupancy.orbital_count == capacity // 2


def test_occupancy_rejects_invalid_subshell():
    with pytest.raises(ValueError):
        SubshellOccupancy.from_electron_count(
            1,
            "p",
            0,
        )


def test_occupancy_orbitals_match_definition():
    occupancy = SubshellOccupancy.from_electron_count(
        3,
        "d",
        5,
    )

    assert tuple(
        orbital.orbital.magnetic_quantum_number
        for orbital in occupancy.orbitals
    ) == occupancy.definition.magnetic_quantum_numbers


def test_electron_subshell_and_occupancy_agree():
    subshell = ElectronSubshell(2, "p", 4)

    occupancy = SubshellOccupancy.from_electron_count(
        subshell.principal_level,
        subshell.subshell,
        subshell.electron_count,
    )

    assert occupancy.capacity == subshell.capacity
    assert occupancy.orbital_count == subshell.orbital_count
    assert occupancy.electron_count == subshell.electron_count


def test_orbital_and_definition_agree():
    definition = define_subshell(3, "d")

    for magnetic_number in definition.magnetic_quantum_numbers:
        orbital = ElectronOrbital(
            3,
            "d",
            magnetic_number,
        )

        assert orbital.angular_momentum_quantum_number == (
            definition.angular_momentum_quantum_number
        )
