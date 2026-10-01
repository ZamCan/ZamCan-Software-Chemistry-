from dataclasses import dataclass
from enum import Enum
class InteractionKind(str,Enum): HYDROGEN_BOND='hydrogen_bond'; HALOGEN_BOND='halogen_bond'; DIPOLE_DIPOLE='dipole_dipole'; ION_DIPOLE='ion_dipole'; VAN_DER_WAALS='van_der_waals'
@dataclass(frozen=True)
class Interaction:
    kind:InteractionKind
    donor:str|None=None
    acceptor:str|None=None
    distance_angstrom:float|None=None
    angle_degrees:float|None=None
    evidence:str=''
    def __post_init__(self):
        if self.distance_angstrom is not None and self.distance_angstrom<=0: raise ValueError('distance must be positive')
        if self.angle_degrees is not None and not 0<=self.angle_degrees<=180: raise ValueError('angle must be 0..180')
