from enum import Enum


class ScientificStatus(str, Enum):
    KNOWN = "known"
    OBSERVED = "observed"
    CALCULATED = "calculated"
    PREDICTED = "predicted"
    HYPOTHESIZED = "hypothesized"


class EvidenceType(str, Enum):
    EXPERIMENTAL = "experimental"
    REFERENCE = "reference"
    COMPUTATIONAL = "computational"
    THEORETICAL = "theoretical"
    OBSERVATIONAL = "observational"


class Phase(str, Enum):
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"
    PLASMA = "plasma"
    SUPERCRITICAL = "supercritical"
    UNKNOWN = "unknown"
