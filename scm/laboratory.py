"""Laboratory protocol metadata, apparatus and safety review records."""
from dataclasses import dataclass, field
from enum import Enum

class SafetyStatus(str,Enum): NOT_REVIEWED='not_reviewed'; REVIEW_REQUIRED='review_required'; REVIEWED='reviewed'; BLOCKED='blocked'
@dataclass(frozen=True)
class Apparatus:
    identifier:str
    name:str
    capacity_value:float|None=None
    capacity_unit:str|None=None
    calibration_due:str|None=None
@dataclass(frozen=True)
class Hazard:
    substance_or_step:str
    hazard:str
    control:str
    source:str=''
@dataclass
class LaboratoryProtocol:
    protocol_id:str
    title:str
    objective:str
    hazards:list[Hazard]=field(default_factory=list)
    required_apparatus:list[Apparatus]=field(default_factory=list)
    safety_status:SafetyStatus=SafetyStatus.NOT_REVIEWED
    reviewer:str|None=None
    def add_hazard(self,hazard:Hazard): self.hazards.append(hazard)
    def mark_reviewed(self,reviewer:str):
        if not reviewer.strip(): raise ValueError('reviewer identity is required')
        if not self.hazards: raise ValueError('hazard review must record at least one hazard or documented no-hazard assessment')
        self.reviewer=reviewer
        self.safety_status=SafetyStatus.REVIEWED
    def block(self): self.safety_status=SafetyStatus.BLOCKED
