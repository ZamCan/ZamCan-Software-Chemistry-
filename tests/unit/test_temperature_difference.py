import pytest

from scm.core.quantity import Quantity
from scm.core.temperature_difference import TemperatureDifference


def test_temperature_difference_normalizes_to_kelvin():
    difference = TemperatureDifference(Quantity(10, "K"))

    assert difference.value == pytest.approx(10)
    assert difference.unit == "K"


def test_temperature_difference_celsius_scale_conversion():
    difference = TemperatureDifference(Quantity(10, "K"))

    result = difference.to("degC")

    assert result.value == pytest.approx(10)


def test_temperature_difference_fahrenheit_scale_conversion():
    difference = TemperatureDifference(Quantity(10, "K"))

    result = difference.to("degF")

    assert result.value == pytest.approx(18)


def test_temperature_difference_addition():
    result = (
        TemperatureDifference(Quantity(10, "K"))
        + TemperatureDifference(Quantity(5, "K"))
    )

    assert result.value == pytest.approx(15)


def test_temperature_difference_subtraction():
    result = (
        TemperatureDifference(Quantity(10, "K"))
        - TemperatureDifference(Quantity(5, "K"))
    )

    assert result.value == pytest.approx(5)


def test_temperature_difference_scaling():
    result = TemperatureDifference(Quantity(10, "K")) * 2

    assert result.value == pytest.approx(20)


def test_temperature_difference_division():
    result = TemperatureDifference(Quantity(10, "K")) / 2

    assert result.value == pytest.approx(5)


def test_temperature_difference_rejects_non_temperature():
    with pytest.raises(ValueError):
        TemperatureDifference(Quantity(10, "m"))


def test_temperature_difference_rejects_non_quantity():
    with pytest.raises(TypeError):
        TemperatureDifference(10)


def test_temperature_difference_negative_is_allowed():
    result = -TemperatureDifference(Quantity(10, "K"))

    assert result.value == pytest.approx(-10)
