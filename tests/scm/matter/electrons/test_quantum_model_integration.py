import pytest

from scm.matter.electrons import (
    ElectronOrbital,
    ElectronSubshell,
    define_subshell,
)


@pytest.mark.parametrize(
    ("designation", "l", "orbital_count", "capacity"),
    [
        ("s", 0, 1, 2),
        ("p", 1, 3, 6),
        ("d", 2, 5, 10),
        ("f", 3, 7, 14),
    ],
)
def test_subshell_uses_canonical_definition(
    designation,
    l,
    orbital_count,
    capacity,
):
    subshell = ElectronSubshell(4, designation, 0)

    assert subshell.definition == define_subshell(4, designation)
    assert subshell.angular_momentum_quantum_number == l
    assert subshell.orbital_count == orbital_count
    assert subshell.capacity == capacity


def test_subshell_rejects_invalid_n_l_combination():
    with pytest.raises(ValueError):
        ElectronSubshell(1, "p", 0)

    with pytest.raises(ValueError):
        ElectronSubshell(2, "d", 0)


def test_subshell_rejects_capacity_overflow():
    with pytest.raises(ValueError):
        ElectronSubshell(2, "p", 7)


def test_subshell_generates_canonical_orbitals():
    subshell = ElectronSubshell(2, "p", 0)

    assert tuple(
        orbital.magnetic_quantum_number
        for orbital in subshell.orbitals
    ) == (-1, 0, 1)


def test_orbital_uses_canonical_definition():
    orbital = ElectronOrbital(3, "d", -2)

    assert orbital.angular_momentum_quantum_number == 2
    assert orbital.magnetic_quantum_number in (
        -2, -1, 0, 1, 2
    )


def test_orbital_rejects_invalid_magnetic_number():
    with pytest.raises(ValueError):
        ElectronOrbital(3, "d", 3)


def test_orbital_rejects_invalid_subshell():
    with pytest.raises(ValueError):
        ElectronOrbital(1, "p", 0)


def test_orbital_capacity_remains_two():
    assert ElectronOrbital(2, "p", 0).capacity == 2
