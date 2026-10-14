"""Validated algebraic methods commonly used in analytical chemistry."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class CalibrationResult:
    slope: float
    intercept: float
    r_squared: float
    observations: int
    def predict(self, response: float) -> float:
        if self.slope == 0: raise ZeroDivisionError('calibration slope is zero')
        return (response-self.intercept)/self.slope

def dilution_concentration(initial_concentration: float, initial_volume: float, final_volume: float) -> float:
    if initial_concentration < 0 or initial_volume < 0 or final_volume <= 0: raise ValueError('concentrations/volumes must be nonnegative and final volume positive')
    return initial_concentration*initial_volume/final_volume

def beer_lambert_concentration(absorbance: float, molar_absorptivity_l_mol_cm: float, path_length_cm: float) -> float:
    if absorbance < 0 or molar_absorptivity_l_mol_cm <= 0 or path_length_cm <= 0: raise ValueError('absorbance must be nonnegative; absorptivity and path length positive')
    return absorbance/(molar_absorptivity_l_mol_cm*path_length_cm)

def calibrate_linear(concentrations: tuple[float,...], responses: tuple[float,...]) -> CalibrationResult:
    if len(concentrations)!=len(responses) or len(concentrations)<2: raise ValueError('at least two paired calibration points are required')
    if any(not math.isfinite(x) for x in concentrations+responses): raise ValueError('calibration data must be finite')
    xm=sum(concentrations)/len(concentrations); ym=sum(responses)/len(responses)
    sxx=sum((x-xm)**2 for x in concentrations); syy=sum((y-ym)**2 for y in responses)
    if sxx==0: raise ValueError('calibration concentrations must not all be identical')
    slope=sum((x-xm)*(y-ym) for x,y in zip(concentrations,responses))/sxx
    intercept=ym-slope*xm
    if syy==0: r2=1.0 if all(y==ym for y in responses) else 0.0
    else: r2=(sum((x-xm)*(y-ym) for x,y in zip(concentrations,responses))**2)/(sxx*syy)
    return CalibrationResult(slope,intercept,r2,len(concentrations))

def ph_from_hydrogen_ion_activity(activity: float) -> float:
    if not math.isfinite(activity) or activity<=0: raise ValueError('hydrogen-ion activity must be finite and positive')
    return -math.log10(activity)
