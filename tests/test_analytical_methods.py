import math

import pytest

from scm.chemistry.analytical_methods import (
    beer_lambert_concentration,
    calibrate_linear,
    dilution_concentration,
    ph_from_hydrogen_ion_activity,
    titration_analyte_concentration,
)


def test_dilution():
    assert dilution_concentration(1.0, 0.01, 0.1) == pytest.approx(0.1)


@pytest.mark.parametrize("args", [
    (-1.0, 1.0, 2.0),
    (1.0, -1.0, 2.0),
    (1.0, 1.0, 0.0),
    (math.inf, 1.0, 2.0),
    (True, 1.0, 2.0),
])
def test_dilution_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        dilution_concentration(*args)


def test_beer_lambert():
    assert beer_lambert_concentration(0.5, 100.0, 1.0) == pytest.approx(0.005)


@pytest.mark.parametrize("args", [
    (-0.1, 100.0, 1.0),
    (0.1, 0.0, 1.0),
    (0.1, 100.0, 0.0),
    (math.nan, 100.0, 1.0),
])
def test_beer_lambert_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        beer_lambert_concentration(*args)


def test_linear_calibration_and_prediction():
    calibration = calibrate_linear((0.0, 1.0, 2.0), (1.0, 3.0, 5.0))
    assert calibration.slope == pytest.approx(2.0)
    assert calibration.intercept == pytest.approx(1.0)
    assert calibration.r_squared == pytest.approx(1.0)
    assert calibration.observations == 3
    assert calibration.predict(7.0) == pytest.approx(3.0)


def test_calibration_constant_response_is_not_reported_as_perfect_fit():
    calibration = calibrate_linear((0.0, 1.0, 2.0), (4.0, 4.0, 4.0))
    assert calibration.slope == pytest.approx(0.0)
    assert calibration.r_squared == 0.0
    with pytest.raises(ZeroDivisionError):
        calibration.predict(4.0)


@pytest.mark.parametrize("concentrations,responses", [
    ((1.0,), (2.0,)),
    ((1.0, 1.0), (2.0, 3.0)),
    ((-1.0, 1.0), (2.0, 3.0)),
    ((0.0, math.inf), (2.0, 3.0)),
    ((0.0, 1.0), (2.0, math.nan)),
    ((0.0, 1.0), (2.0,)),
])
def test_calibration_rejects_invalid_data(concentrations, responses):
    with pytest.raises(ValueError):
        calibrate_linear(concentrations, responses)


def test_titration_one_to_one():
    # 0.100 mol/L titrant, 25.00 mL used for a 20.00 mL sample.
    assert titration_analyte_concentration(0.100, 25.00, 20.00) == pytest.approx(0.125)


def test_titration_non_one_to_one_stoichiometry():
    # For 2 analyte units per titrant unit, analyte concentration is doubled.
    assert titration_analyte_concentration(0.100, 10.0, 20.0, 2.0) == pytest.approx(0.100)


@pytest.mark.parametrize("args", [
    (-0.1, 10.0, 20.0, 1.0),
    (0.1, -10.0, 20.0, 1.0),
    (0.1, 10.0, 0.0, 1.0),
    (0.1, 10.0, 20.0, 0.0),
    (math.inf, 10.0, 20.0, 1.0),
])
def test_titration_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        titration_analyte_concentration(*args)


def test_ph():
    assert ph_from_hydrogen_ion_activity(1e-7) == pytest.approx(7.0)


@pytest.mark.parametrize("activity", [0, -1, math.inf, math.nan, True])
def test_invalid_ph_activity(activity):
    with pytest.raises(ValueError):
        ph_from_hydrogen_ion_activity(activity)
