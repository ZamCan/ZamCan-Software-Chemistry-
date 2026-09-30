import pytest

from scm.core.quantity import Quantity
from scm.core.units import Dimension


def test_quantity_conversion():
    quantity = Quantity(1000, "mg")

    result = quantity.to("g")

    assert result.value == pytest.approx(1.0)
    assert result.unit == "g"


def test_quantity_addition_with_conversion():
    result = Quantity(1000, "mg") + Quantity(1, "g")

    assert result.value == pytest.approx(2000.0)
    assert result.unit == "mg"


def test_quantity_subtraction():
    result = Quantity(2, "kg") - Quantity(500, "g")

    assert result.value == pytest.approx(1.5)
    assert result.unit == "kg"


def test_incompatible_addition_fails():
    with pytest.raises(ValueError):
        Quantity(1, "kg") + Quantity(1, "m")


def test_dimension_is_available():
    quantity = Quantity(5, "g")

    assert quantity.dimension == Dimension(mass=1)


def test_mass_density_dimension():
    density = Quantity(5, "kg") / Quantity(2, "L")

    assert density.dimension == Dimension(mass=1, length=-3)


def test_electric_charge_is_current_times_time():
    from scm.core.units import CHARGE, CURRENT, TIME

    assert CHARGE == CURRENT * TIME


def test_coulomb_has_charge_dimension():
    from scm.core import Quantity
    from scm.core.units import CHARGE

    charge = Quantity(1, "C")

    assert charge.dimension == CHARGE


def test_ampere_second_is_coulomb_dimension():
    from scm.core import Quantity
    from scm.core.units import CHARGE

    charge = Quantity(1, "A") * Quantity(1, "s")

    assert charge.dimension == CHARGE
    assert charge.unit == "C"


def test_coulomb_cannot_be_added_to_ampere():
    from scm.core import Quantity
    import pytest

    with pytest.raises(ValueError):
        Quantity(1, "C") + Quantity(1, "A")


def test_quantity_equality_ignores_cached_dimension_representation():
    from scm.core import Quantity

    assert Quantity(2, "m") == Quantity(2, "m")


def test_quantity_equality_converts_units():
    from scm.core import Quantity

    assert Quantity(1, "m") == Quantity(100, "cm")
    assert Quantity(1, "m") == Quantity(1000, "mm")


def test_quantity_equality_rejects_different_dimensions():
    from scm.core import Quantity

    assert Quantity(1, "m") != Quantity(1, "s")


def test_nanometer_unit():
    from scm.core import Quantity

    assert Quantity(1, "nm").to("m").value == 1e-9
    assert Quantity(1, "m").to("nm").value == 1e9


def test_absolute_temperature_addition_is_rejected():
    with pytest.raises(ValueError):
        Quantity(25, "degC") + Quantity(10, "degC")


def test_absolute_temperature_subtraction_returns_difference():
    result = Quantity(25, "degC") - Quantity(10, "degC")

    from scm.core.temperature_difference import TemperatureDifference

    assert isinstance(result, TemperatureDifference)
    assert result.value == pytest.approx(15)


def test_absolute_temperature_subtraction_between_celsius_and_kelvin():
    result = Quantity(25, "degC") - Quantity(298.15, "K")

    from scm.core.temperature_difference import TemperatureDifference

    assert isinstance(result, TemperatureDifference)
    assert result.value == pytest.approx(0)


def test_absolute_temperature_can_add_temperature_difference():
    from scm.core.temperature_difference import TemperatureDifference

    result = Quantity(25, "degC") + TemperatureDifference(
        Quantity(10, "K")
    )

    assert result.value == pytest.approx(35)
    assert result.unit == "degC"


def test_temperature_difference_can_be_added_to_absolute_temperature():
    from scm.core.temperature_difference import TemperatureDifference

    result = TemperatureDifference(
        Quantity(10, "K")
    ) + Quantity(25, "degC")

    assert result.value == pytest.approx(35)
    assert result.unit == "degC"


def test_absolute_temperature_multiplication_is_rejected():
    with pytest.raises(ValueError):
        Quantity(25, "degC") * 2


def test_absolute_temperature_division_is_rejected():
    with pytest.raises(ValueError):
        Quantity(25, "degC") / 2
