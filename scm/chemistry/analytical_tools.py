from dataclasses import dataclass
import math
@dataclass(frozen=True)
class DilutionResult:
    final_volume_l:float
    final_concentration_mol_l:float
def dilution(initial_concentration,initial_volume_l,final_volume_l):
    if min(initial_concentration,initial_volume_l,final_volume_l)<=0: raise ValueError('inputs must be positive')
    return DilutionResult(final_volume_l,initial_concentration*initial_volume_l/final_volume_l)
@dataclass(frozen=True)
class BeerLambertResult:
    absorbance:float
    concentration_mol_l:float
def beer_lambert(molar_absorptivity,path_length_cm,concentration_mol_l):
    if min(molar_absorptivity,path_length_cm,concentration_mol_l)<0: raise ValueError('inputs must be nonnegative')
    return BeerLambertResult(molar_absorptivity*path_length_cm*concentration_mol_l,concentration_mol_l)
def ph_from_hydrogen_activity(activity):
    if activity<=0: raise ValueError('activity must be positive')
    return -math.log10(activity)
def pOH_from_hydroxide_activity(activity):
    if activity<=0: raise ValueError('activity must be positive')
    return -math.log10(activity)
