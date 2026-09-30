import math

import pytest

from scm.core import Quantity
from scm.core.units import ANGLE, Dimension, get_unit


def test_angle_dimension_is_explicit():
    assert ANGLE == Dimension(angle=1)
    assert get_unit("rad").dimension == ANGLE
    assert get_unit("deg").dimension == ANGLE


def test_radian_is_canonical_angle_unit():
    assert get_unit("rad").scale == 1.0


def test_degrees_have_correct_radian_scale():
    assert get_unit("deg").scale == pytest.approx(math.pi / 180.0)


def test_degrees_to_radians():
    angle = Quantity(180.0, "deg")

    converted = angle.to("rad")

    assert converted.value == pytest.approx(math.pi)
    assert converted.unit == "rad"


def test_radians_to_degrees():
    angle = Quantity(math.pi, "rad")

    converted = angle.to("deg")

    assert converted.value == pytest.approx(180.0)
    assert converted.unit == "deg"


def test_right_angle_conversion():
    angle = Quantity(90.0, "deg")

    converted = angle.to("rad")

    assert converted.value == pytest.approx(math.pi / 2.0)


def test_angle_quantity_rejects_non_angle_conversion():
    angle = Quantity(90.0, "deg")

    with pytest.raises(ValueError):
        angle.to("m")


def test_angle_quantity_is_not_equal_to_dimensionless_quantity():
    angle = Quantity(1.0, "rad")
    dimensionless = Quantity(1.0, "1")

    assert angle != dimensionless


def test_angle_addition_requires_angle_dimension():
    first = Quantity(30.0, "deg")
    second = Quantity(60.0, "deg")

    result = first + second

    assert result.value == pytest.approx(90.0)
    assert result.unit == "deg"


def test_angle_addition_across_units():
    first = Quantity(90.0, "deg")
    second = Quantity(math.pi / 2.0, "rad")

    result = first + second

    assert result.value == pytest.approx(180.0)
    assert result.unit == "deg"


def test_angle_subtraction_across_units():
    first = Quantity(180.0, "deg")
    second = Quantity(math.pi / 2.0, "rad")

    result = first - second

    assert result.value == pytest.approx(90.0)
    assert result.unit == "deg"
