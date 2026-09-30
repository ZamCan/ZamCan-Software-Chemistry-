import pytest

from scm.core.quantity import Quantity
from scm.core.units import (
    AMOUNT,
    LENGTH,
    MASS,
    Dimension,
    convert,
    get_unit,
)


def test_mass_conversion():
    assert convert(1000, "mg", "g") == pytest.approx(1.0)


def test_volume_conversion():
    assert convert(1000, "mL", "L") == pytest.approx(1.0)


def test_energy_conversion():
    assert convert(1, "kJ", "J") == pytest.approx(1000.0)


def test_dimension_relationships():
    density = MASS / (LENGTH * LENGTH * LENGTH)

    assert density == Dimension(mass=1, length=-3)


def test_incompatible_conversion_fails():
    with pytest.raises(ValueError):
        convert(1, "kg", "m")


def test_amount_dimension():
    assert AMOUNT.amount == 1


def test_celsius_to_kelvin_conversion():
    assert convert(0.0, "degC", "K") == pytest.approx(273.15)
    assert convert(25.0, "degC", "K") == pytest.approx(298.15)


def test_kelvin_to_celsius_conversion():
    assert convert(273.15, "K", "degC") == pytest.approx(0.0)
    assert convert(298.15, "K", "degC") == pytest.approx(25.0)


def test_fahrenheit_to_celsius_conversion():
    assert convert(32.0, "degF", "degC") == pytest.approx(0.0)
    assert convert(212.0, "degF", "degC") == pytest.approx(100.0)


def test_celsius_to_fahrenheit_conversion():
    assert convert(0.0, "degC", "degF") == pytest.approx(32.0)
    assert convert(100.0, "degC", "degF") == pytest.approx(212.0)


def test_quantity_uses_offset_aware_temperature_conversion():
    temperature = Quantity(25.0, "degC")

    converted = temperature.to("K")

    assert converted.value == pytest.approx(298.15)
    assert converted.unit == "K"


def test_temperature_units_have_same_dimension():
    assert get_unit("K").dimension == get_unit("degC").dimension
    assert get_unit("K").dimension == get_unit("degF").dimension


def test_temperature_conversion_rejects_incompatible_dimension():
    with pytest.raises(ValueError):
        convert(25.0, "degC", "kg")
