from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AnalysisType(str, Enum):
    QUALITATIVE = "qualitative"
    QUANTITATIVE = "quantitative"
    VOLUMETRIC = "volumetric"
    GRAVIMETRIC = "gravimetric"


@dataclass(frozen=True)
class Observation:
    test: str
    observation: str

    def __post_init__(self) -> None:
        if not self.test.strip():
            raise ValueError("test must not be empty")

        if not self.observation.strip():
            raise ValueError("observation must not be empty")


@dataclass(frozen=True)
class AnalysisRecord:
    analysis_type: AnalysisType
    observations: tuple[Observation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.analysis_type, AnalysisType):
            raise TypeError("analysis_type must be an AnalysisType")

        for observation in self.observations:
            if not isinstance(observation, Observation):
                raise TypeError(
                    "observations must contain Observation instances"
                )
