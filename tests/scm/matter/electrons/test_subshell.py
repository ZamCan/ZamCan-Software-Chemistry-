import pytest

from scm.matter.electrons import (
    SubshellDefinition,
    define_subshell,
)


@pytest.mark.parametrize(
    ("designation", "l", "orbitals", "capacity"),
    [
        ("s", 0, 1, 2),
        ("p", 1, 3, 6),
        ("d", 2, 5, 10),
        ("f", 3, 7, 14),
    ],
)
def test_subshell_definition(
    designation,
    l,
    orbitals,
    capacity,
):
    definition = define_subshell(4, designation)

    assert definition.designation == designation
    assert definition.angular_momentum_quantum_number == l
    assert definition.orbital_count == orbitals
    assert definition.electron_capacity == capacity


def test_magnetic_quantum_numbers():
    assert define_subshell(2, "s").magnetic_quantum_numbers == (0,)
    assert define_subshell(2, "p").magnetic_quantum_numbers == (-1, 0, 1)
    assert define_subshell(3, "d").magnetic_quantum_numbers == (
        -2, -1, 0, 1, 2
    )
    assert define_subshell(4, "f").magnetic_quantum_numbers == (
        -3, -2, -1, 0, 1, 2, 3
    )


def test_label():
    assert define_subshell(3, "p").label == "3p"


def test_designation_is_normalized():
    assert define_subshell(3, " P ").designation == "p"


def test_invalid_designation():
    with pytest.raises(ValueError):
        define_subshell(2, "g")


def test_invalid_quantum_relationship():
    with pytest.raises(ValueError):
        SubshellDefinition(
            principal_level=1,
            designation="p",
            angular_momentum_quantum_number=1,
        )


def test_mismatched_l_and_designation():
    with pytest.raises(ValueError):
        SubshellDefinition(
            principal_level=3,
            designation="p",
            angular_momentum_quantum_number=2,
        )


def test_invalid_principal_level():
    with pytest.raises(ValueError):
        define_subshell(0, "s")
