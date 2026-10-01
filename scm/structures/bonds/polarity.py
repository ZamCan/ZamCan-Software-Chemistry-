"""Geometry-aware polarity primitives. Partial charges are never invented."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class DipoleVector:
    x:float; y:float; z:float
    @property
    def magnitude(self): return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
@dataclass(frozen=True)
class PolarityAssessment:
    net_dipole:DipoleVector|None
    status:str
    reason:str
def assess_polarity(dipoles):
    if not dipoles: return PolarityAssessment(None,'insufficient_data','No bond dipoles were supplied.')
    total=DipoleVector(sum(d.x for d in dipoles),sum(d.y for d in dipoles),sum(d.z for d in dipoles))
    return PolarityAssessment(total,'calculated','Net dipole is the vector sum of supplied bond dipoles.')
