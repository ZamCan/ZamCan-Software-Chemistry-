import pytest
from scm.chemistry.analytical_methods import dilution_concentration, beer_lambert_concentration, calibrate_linear, ph_from_hydrogen_ion_activity

def test_dilution(): assert dilution_concentration(1.0,0.01,0.1)==pytest.approx(0.1)
def test_beer_lambert(): assert beer_lambert_concentration(0.5,100.0,1.0)==pytest.approx(0.005)
def test_calibration():
    c=calibrate_linear((0.0,1.0,2.0),(1.0,3.0,5.0))
    assert c.slope==pytest.approx(2.0)
    assert c.intercept==pytest.approx(1.0)
    assert c.r_squared==pytest.approx(1.0)
    assert c.predict(7.0)==pytest.approx(3.0)
def test_ph(): assert ph_from_hydrogen_ion_activity(1e-7)==pytest.approx(7.0)
def test_invalid_ph_activity():
    with pytest.raises(ValueError): ph_from_hydrogen_ion_activity(0)
