from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Uncertainty:
    absolute: Optional[float] = None
    relative: Optional[float] = None
    confidence: Optional[float] = None

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
