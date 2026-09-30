from __future__ import annotations

import pytest

from scm.matter.electrons import ElectronOrbital


def test_s_orbital_has_one_orbital():
    orbital = ElectronOrbital(
        principal_level=1,
        subshell="s",
        magnetic_quantum_number=0,
    )

    assert orbital.label == "1s(m=0)"
    assert orbital.capacity == 2


def test_p_subshell_has_three_allowed_orbitals():
    orbitals = tuple(
        ElectronOrbital(
            principal_level=2,
            subshell="p",
            magnetic_quantum_number=m,
        )
        for m in (-1, 0, 1)
    )

    assert len(orbitals) == 3
    assert all(orbital.capacity == 2 for orbital in orbitals)


def test_d_subshell_has_five_allowed_orbitals():
    orbitals = tuple(
        ElectronOrbital(
            principal_level=3,
            subshell="d",
            magnetic_quantum_number=m,
        )
        for m in (-2, -1, 0, 1, 2)
    )

    assert len(orbitals) == 5


def test_f_subshell_has_seven_allowed_orbitals():
    orbitals = tuple(
        ElectronOrbital(
            principal_level=4,
            subshell="f",
            magnetic_quantum_number=m,
        )
        for m in (-3, -2, -1, 0, 1, 2, 3)
    )

    assert len(orbitals) == 7


def test_orbital_rejects_invalid_magnetic_quantum_number():
    with pytest.raises(ValueError):
        ElectronOrbital(
            principal_level=2,
            subshell="p",
            magnetic_quantum_number=2,
        )


def test_orbital_rejects_nonexistent_1p():
    with pytest.raises(ValueError):
        ElectronOrbital(
            principal_level=1,
            subshell="p",
            magnetic_quantum_number=0,
        )


def test_orbital_rejects_invalid_subshell():
    with pytest.raises(ValueError):
        ElectronOrbital(
            principal_level=2,
            subshell="g",
            magnetic_quantum_number=0,
        )


def test_orbital_allows_zero_or_two_electrons_only():
    with pytest.raises(ValueError):
        ElectronOrbital(
            principal_level=1,
            subshell="s",
            magnetic_quantum_number=0,
            electron_count=3,
        )


def test_orbital_accepts_zero_electrons():
    orbital = ElectronOrbital(
        principal_level=1,
        subshell="s",
        magnetic_quantum_number=0,
        electron_count=0,
    )

    assert orbital.electron_count == 0


def test_orbital_accepts_two_electrons():
    orbital = ElectronOrbital(
        principal_level=1,
        subshell="s",
        magnetic_quantum_number=0,
        electron_count=2,
    )

    assert orbital.electron_count == 2

def test_s_subshell_contains_one_orbital():
    from scm.matter.electrons import ElectronSubshell

    subshell = ElectronSubshell(
        principal_level=1,
        subshell="s",
        electron_count=2,
    )

    assert subshell.angular_momentum_quantum_number == 0
    assert subshell.orbital_count == 1
    assert len(subshell.orbitals) == 1
    assert subshell.orbitals[0].magnetic_quantum_number == 0


def test_p_subshell_contains_three_orbitals():
    from scm.matter.electrons import ElectronSubshell

    subshell = ElectronSubshell(
        principal_level=2,
        subshell="p",
        electron_count=6,
    )

    assert subshell.angular_momentum_quantum_number == 1
    assert subshell.orbital_count == 3

    assert tuple(
        orbital.magnetic_quantum_number
        for orbital in subshell.orbitals
    ) == (-1, 0, 1)


def test_d_subshell_contains_five_orbitals():
    from scm.matter.electrons import ElectronSubshell

    subshell = ElectronSubshell(
        principal_level=3,
        subshell="d",
        electron_count=10,
    )

    assert subshell.orbital_count == 5


def test_f_subshell_contains_seven_orbitals():
    from scm.matter.electrons import ElectronSubshell

    subshell = ElectronSubshell(
        principal_level=4,
        subshell="f",
        electron_count=14,
    )

    assert subshell.orbital_count == 7

