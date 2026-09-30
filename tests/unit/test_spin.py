from fractions import Fraction

import pytest

from scm.matter.particles import Spin


def test_spin_half_allowed_projections():
    spin = Spin(Fraction(1, 2))

    assert spin.quantum_number == Fraction(1, 2)
    assert spin.allowed_projections == (
        Fraction(-1, 2),
        Fraction(1, 2),
    )


def test_spin_zero_has_one_projection():
    spin = Spin(Fraction(0))

    assert spin.allowed_projections == (
        Fraction(0),
    )


def test_spin_one_allowed_projections():
    spin = Spin(Fraction(1))

    assert spin.allowed_projections == (
        Fraction(-1),
        Fraction(0),
        Fraction(1),
    )


def test_spin_three_halves_allowed_projections():
    spin = Spin(Fraction(3, 2))

    assert spin.allowed_projections == (
        Fraction(-3, 2),
        Fraction(-1, 2),
        Fraction(1, 2),
        Fraction(3, 2),
    )


def test_spin_projection_must_be_valid():
    Spin(Fraction(1, 2), Fraction(-1, 2))
    Spin(Fraction(1, 2), Fraction(1, 2))

    with pytest.raises(ValueError):
        Spin(Fraction(1, 2), Fraction(3, 2))

    with pytest.raises(ValueError):
        Spin(Fraction(1, 2), Fraction(0))


def test_spin_magnitude_is_angular_momentum():
    spin = Spin(Fraction(1, 2))

    magnitude = spin.angular_momentum_magnitude

    assert magnitude.unit == "J·s"
    assert magnitude.value > 0


def test_invalid_spin_quantum_number_is_rejected():
    with pytest.raises(ValueError):
        Spin(Fraction(3, 10))

    with pytest.raises(ValueError):
        Spin(Fraction(7, 4))


def test_negative_spin_quantum_number_is_rejected():
    with pytest.raises(ValueError):
        Spin(Fraction(-1, 2))


def test_spin_requires_fraction():
    with pytest.raises(TypeError):
        Spin(0.5)
