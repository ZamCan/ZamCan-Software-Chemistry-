from dataclasses import dataclass
from typing import Optional

from .quantity import Quantity


@dataclass(frozen=True)
class Conditions:
    temperature: Optional[Quantity] = None
    pressure: Optional[Quantity] = None
    volume: Optional[Quantity] = None
    pH: Optional[float] = None
    solvent: Optional[str] = None
    atmosphere: Optional[str] = None
