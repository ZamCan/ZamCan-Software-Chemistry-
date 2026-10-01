from dataclasses import dataclass, field

@dataclass(frozen=True)
class Apparatus:
    apparatus_id:str
    name:str
    capacity:float|None=None
    unit:str|None=None
    precision:float|None=None

@dataclass(frozen=True)
class Measurement:
    quantity:str
    value:float
    unit:str
    instrument_id:str|None=None
    uncertainty:float|None=None

@dataclass
class Instrument:
    instrument_id:str
    name:str
    measurements:list[Measurement]=field(default_factory=list)
    def record(self,m): self.measurements.append(m)
