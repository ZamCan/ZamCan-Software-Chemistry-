import pytest

from scm.matter.electrons import (
    ElectronOrbital,
    ElectronSpin,
    OrbitalOccupancy,
    SubshellOccupancy,
)


def test_empty_orbital():
    orbital = ElectronOrbital(2, "p", -1, 0)
    occupancy = OrbitalOccupancy.empty(orbital)

    assert occupancy.electron_count == 0
    assert occupancy.is_empty
    assert occupancy.spins == ()


def test_single_orbital_with_up_spin():
    orbital = ElectronOrbital(2, "p", -1, 1)
    occupancy = OrbitalOccupancy.single(orbital, ElectronSpin.UP)

    assert occupancy.electron_count == 1
    assert occupancy.is_singly_occupied
    assert occupancy.spins == (ElectronSpin.UP,)


def test_single_orbital_with_down_spin():
    orbital = ElectronOrbital(2, "p", 0, 1)
    occupancy = OrbitalOccupancy.single(orbital, ElectronSpin.DOWN)

    assert occupancy.spins == (ElectronSpin.DOWN,)


def test_double_orbital_has_opposite_spins():
    orbital = ElectronOrbital(2, "p", 1, 2)
    occupancy = OrbitalOccupancy.double(orbital)

    assert occupancy.electron_count == 2
    assert occupancy.is_doubly_occupied
    assert occupancy.spins == (
        ElectronSpin.UP,
        ElectronSpin.DOWN,
    )


def test_double_orbital_rejects_same_spin():
    orbital = ElectronOrbital(2, "p", 1, 2)

    with pytest.raises(ValueError):
        OrbitalOccupancy(
            orbital=orbital,
            electrons=(
                __import__(
                    "scm.matter.electrons",
                    fromlist=["OrbitalElectron"],
                ).OrbitalElectron(ElectronSpin.UP),
                __import__(
                    "scm.matter.electrons",
                    fromlist=["OrbitalElectron"],
                ).OrbitalElectron(ElectronSpin.UP),
            ),
        )


def test_p_subshell_orbital_count_and_capacity():
    subshell = SubshellOccupancy.from_electron_count(2, "p", 0)

    assert subshell.orbital_count == 3
    assert subshell.capacity == 6
    assert subshell.electron_count == 0


@pytest.mark.parametrize(
    ("electron_count", "expected_unpaired"),
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 2),
        (5, 1),
        (6, 0),
    ],
)
def test_p_subshell_hund_distribution(electron_count, expected_unpaired):
    subshell = SubshellOccupancy.from_electron_count(
        2,
        "p",
        electron_count,
    )

    assert subshell.electron_count == electron_count
    assert subshell.unpaired_electron_count == expected_unpaired
    assert subshell.validate_pauli()
    assert subshell.validate_hund()
    assert subshell.is_hund_ground_state


@pytest.mark.parametrize(
    ("subshell", "capacity"),
    [
        ("s", 2),
        ("p", 6),
        ("d", 10),
        ("f", 14),
    ],
)
def test_subshell_capacities(subshell, capacity):
    occupancy = SubshellOccupancy.from_electron_count(
        4,
        subshell,
        capacity,
    )

    assert occupancy.electron_count == capacity
    assert occupancy.capacity == capacity
    assert occupancy.unpaired_electron_count == 0


def test_invalid_subshell_quantum_numbers():
    with pytest.raises(ValueError):
        SubshellOccupancy.from_electron_count(1, "p", 1)

    with pytest.raises(ValueError):
        SubshellOccupancy.from_electron_count(2, "d", 1)


def test_invalid_electron_count():
    with pytest.raises(ValueError):
        SubshellOccupancy.from_electron_count(2, "p", -1)

    with pytest.raises(ValueError):
        SubshellOccupancy.from_electron_count(2, "p", 7)


def test_notation():
    occupancy = SubshellOccupancy.from_electron_count(2, "p", 3)

    assert occupancy.notation == "2p3"


def test_spin_multiplicity():
    assert (
        SubshellOccupancy.from_electron_count(2, "p", 3)
        .spin_multiplicity
        == 4
    )

    assert (
        SubshellOccupancy.from_electron_count(2, "p", 4)
        .spin_multiplicity
        == 3
    )
