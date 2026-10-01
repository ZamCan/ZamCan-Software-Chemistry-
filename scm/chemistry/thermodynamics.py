from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math
class ThermoStatus(str,Enum): CALCULATED="calculated"; INSUFFICIENT_DATA="insufficient_data"
@dataclass(frozen=True)
class ThermodynamicResult:
    delta_h:float|None; delta_s:float|None; delta_g:float|None; temperature_k:float; status:ThermoStatus; explanation:str
def gibbs_free_energy(delta_h:float,delta_s:float,temperature_k:float)->float:
    if temperature_k<=0: raise ValueError("temperature must be > 0 K")
    return delta_h-temperature_k*delta_s
def reaction_thermodynamics(delta_h,delta_s,temperature_k):
    dg=gibbs_free_energy(delta_h,delta_s,temperature_k) if delta_h is not None and delta_s is not None else None
    return ThermodynamicResult(delta_h,delta_s,dg,temperature_k,ThermoStatus.CALCULATED if dg is not None else ThermoStatus.INSUFFICIENT_DATA,"ΔG = ΔH − TΔS.")
def equilibrium_constant_from_delta_g(delta_g_j_mol,temperature_k,r=8.314462618):
    if temperature_k<=0 or r<=0: raise ValueError("invalid temperature or gas constant")
    return math.exp(-delta_g_j_mol/(r*temperature_k))
