"""Validated algebraic methods commonly used in analytical chemistry.

These methods deliberately expose their assumptions and reject invalid numeric
inputs. They are calculation primitives, not a substitute for method validation
or review of laboratory quality-control data.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def _finite_real(value: object, name: str) -> float:
    """Return a finite float while rejecting booleans and non-real values."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite real number")
    return result


@dataclass(frozen=True)
class CalibrationResult:
    """Ordinary least-squares calibration: response = slope * concentration + intercept.

    r_squared is set to 0.0 when responses have no variation: goodness of fit
    is undefined in that case, and reporting a perfect fit would be misleading.
    """
    slope: float
    intercept: float
    r_squared: float
    observations: int

    def predict(self, response: float) -> float:
        """Infer concentration from a measured response using this calibration."""
        response = _finite_real(response, "response")
        if self.slope == 0:
            raise ZeroDivisionError("calibration slope is zero")
        return (response - self.intercept) / self.slope


def dilution_concentration(
    initial_concentration: float,
    initial_volume: float,
    final_volume: float,
) -> float:
    """Calculate final concentration using C1V1=C2V2 and consistent units."""
    c1 = _finite_real(initial_concentration, "initial_concentration")
    v1 = _finite_real(initial_volume, "initial_volume")
    v2 = _finite_real(final_volume, "final_volume")
    if c1 < 0 or v1 < 0 or v2 <= 0:
        raise ValueError("concentration and initial volume must be nonnegative; final volume must be positive")
    return c1 * v1 / v2


def beer_lambert_concentration(
    absorbance: float,
    molar_absorptivity_l_mol_cm: float,
    path_length_cm: float,
) -> float:
    """Calculate concentration from A = epsilon*l*c when Beer-Lambert applies."""
    a = _finite_real(absorbance, "absorbance")
    epsilon = _finite_real(molar_absorptivity_l_mol_cm, "molar absorptivity")
    path = _finite_real(path_length_cm, "path length")
    if a < 0 or epsilon <= 0 or path <= 0:
        raise ValueError("absorbance must be nonnegative; absorptivity and path length positive")
    return a / (epsilon * path)


def titration_analyte_concentration(
    titrant_concentration: float,
    titrant_volume: float,
    analyte_volume: float,
    analyte_to_titrant_coefficient_ratio: float = 1.0,
) -> float:
    """Calculate analyte concentration at stoichiometric equivalence.

    The coefficient ratio is nu(analyte)/nu(titrant) from the balanced reaction.
    Use consistent volume units. Assumes a valid equivalence point, known
    stoichiometry, and no unaccounted side reactions.
    """
    concentration = _finite_real(titrant_concentration, "titrant_concentration")
    delivered = _finite_real(titrant_volume, "titrant_volume")
    sample = _finite_real(analyte_volume, "analyte_volume")
    ratio = _finite_real(analyte_to_titrant_coefficient_ratio, "analyte_to_titrant_coefficient_ratio")
    if concentration < 0 or delivered < 0 or sample <= 0 or ratio <= 0:
        raise ValueError("titrant concentration and volume must be nonnegative; analyte volume and coefficient ratio must be positive")
    return concentration * delivered * ratio / sample


def calibrate_linear(
    concentrations: tuple[float, ...],
    responses: tuple[float, ...],
) -> CalibrationResult:
    """Fit an ordinary least-squares straight line to paired calibration data."""
    if len(concentrations) != len(responses) or len(concentrations) < 2:
        raise ValueError("at least two paired calibration points are required")
    xs = tuple(_finite_real(x, "calibration concentration") for x in concentrations)
    ys = tuple(_finite_real(y, "calibration response") for y in responses)
    if any(x < 0 for x in xs):
        raise ValueError("calibration concentrations must be nonnegative")
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    sxx = sum((x - x_mean) ** 2 for x in xs)
    syy = sum((y - y_mean) ** 2 for y in ys)
    if sxx == 0:
        raise ValueError("calibration concentrations must not all be identical")
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    r_squared = (sxy * sxy) / (sxx * syy) if syy > 0 else 0.0
    r_squared = min(1.0, max(0.0, r_squared))
    return CalibrationResult(slope, intercept, r_squared, len(xs))


def ph_from_hydrogen_ion_activity(activity: float) -> float:
    """Calculate pH = -log10(a_H+); activity is dimensionless."""
    value = _finite_real(activity, "hydrogen-ion activity")
    if value <= 0:
        raise ValueError("hydrogen-ion activity must be finite and positive")
    return -math.log10(value)
