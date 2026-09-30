from fractions import Fraction

import pytest

from scm.core import Quantity
from scm.matter.particles import Particle, Spin


def test_particle_creation():
    electron = Particle(
        name="electron",
        symbol="e⁻",
        rest_mass=Quantity(9.1093837e-31, "kg"),
        elementary_charge_number=-1,
        intrinsic_spin=Spin(Fraction(1, 2)),
    )

    assert electron.name == "electron"
    assert electron.symbol == "e⁻"
    assert electron.rest_mass.value > 0
    assert electron.rest_mass.unit == "kg"

    assert electron.elementary_charge_number == -1
    assert electron.charge_symbol == "-e"
    assert electron.electric_charge.unit == "C"
    assert electron.electric_charge.value == pytest.approx(
        -1.602176634e-19
    )

    assert electron.intrinsic_spin is not None
    assert electron.intrinsic_spin.quantum_number == Fraction(1, 2)
    assert electron.intrinsic_spin.allowed_projections == (
        Fraction(-1, 2),
        Fraction(1, 2),
    )


def test_particle_string_representation():
    particle = Particle(
        name="test particle",
        symbol="X",
        rest_mass=Quantity(1, "kg"),
        elementary_charge_number=0,
    )

    assert str(particle) == "X"
    assert particle.charge_symbol == "0"
    assert particle.electric_charge.value == 0
    assert particle.electric_charge.unit == "C"
    assert particle.intrinsic_spin is None


def test_positive_elementary_charge():
    proton = Particle(
        name="proton",
        symbol="p⁺",
        rest_mass=Quantity(1.67262192369e-27, "kg"),
        elementary_charge_number=1,
        intrinsic_spin=Spin(Fraction(1, 2)),
    )

    assert proton.charge_symbol == "+e"
    assert proton.electric_charge.value == pytest.approx(
        1.602176634e-19
    )
    assert proton.electric_charge.unit == "C"

    assert proton.intrinsic_spin is not None
    assert proton.intrinsic_spin.quantum_number == Fraction(1, 2)


def test_multiple_elementary_charges():
    particle = Particle(
        name="test ion",
        symbol="X²⁺",
        rest_mass=Quantity(1, "kg"),
        elementary_charge_number=2,
    )

    assert particle.charge_symbol == "+2e"
    assert particle.electric_charge.value == pytest.approx(
        3.204353268e-19
    )
    assert particle.electric_charge.unit == "C"
    assert particle.intrinsic_spin is None
