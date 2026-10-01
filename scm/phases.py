from dataclasses import dataclass
from enum import Enum
class Phase(str,Enum): SOLID='solid'; LIQUID='liquid'; GAS='gas'; PLASMA='plasma'; SUPERCRITICAL='supercritical'; UNKNOWN='unknown'
@dataclass(frozen=True)
class PhaseState:
    phase:Phase
    temperature_k:float|None=None
    pressure_pa:float|None=None
    evidence:str=''
    def __post_init__(self):
        if self.temperature_k is not None and self.temperature_k<=0: raise ValueError('temperature must be > 0 K')
        if self.pressure_pa is not None and self.pressure_pa<=0: raise ValueError('pressure must be > 0 Pa')
