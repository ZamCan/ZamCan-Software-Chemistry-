from scm.core import Quantity
from zcm.chemistry.calculator import chemistry_calculator


def test_calculator_addition():
    result = chemistry_calculator.add(
        Quantity(5, "g"),
        Quantity(2, "g"),
    )

    assert result.value == 7
    assert result.unit == "g"


def test_calculator_conversion_aware_addition():
    result = chemistry_calculator.add(
        Quantity(1, "kg"),
        Quantity(500, "g"),
    )

    assert result.value == 1.5
    assert result.unit == "kg"


def test_calculator_multiplication():
    result = chemistry_calculator.multiply(
        Quantity(2, "mol"),
        Quantity(3, "mol⁻¹"),
    )

    assert result.value == 6
    assert result.unit == "1"
