from __future__ import annotations
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class RateResult:
    rate:float; order:int
def rate_law(k,concentrations,orders)->RateResult:
    if k<0 or len(concentrations)!=len(orders) or any(c<0 or o<0 for c,o in zip(concentrations,orders)): raise ValueError("invalid rate-law inputs")
    rate=k
    for c,o in zip(concentrations,orders): rate*=c**o
    return RateResult(rate,sum(orders))
def arrhenius_rate(k0,activation_energy_j_mol,temperature_k,r=8.314462618):
    if k0<0 or temperature_k<=0 or r<=0: raise ValueError("invalid Arrhenius inputs")
    return k0*math.exp(-activation_energy_j_mol/(r*temperature_k))
