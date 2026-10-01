from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ElectronGeometry(str, Enum):
    LINEAR = "linear"
    TRIGONAL_PLANAR = "trigonal_planar"
    TETRAHEDRAL = "tetrahedral"
    TRIGONAL_BIPYRAMIDAL = "trigonal_bipyramidal"
    OCTAHEDRAL = "octahedral"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class VSEPRResult:
    steric_number: int
    bonding_domains: int
    lone_pair_domains: int
    electron_geometry: ElectronGeometry
    molecular_geometry: str
    explanation: str


def analyze_vsepr(bonding_domains: int, lone_pair_domains: int) -> VSEPRResult:
    if isinstance(bonding_domains, bool) or isinstance(lone_pair_domains, bool):
        raise TypeError("domain counts must be integers")
    if bonding_domains < 0 or lone_pair_domains < 0:
        raise ValueError("domain counts must be nonnegative")
    steric = bonding_domains + lone_pair_domains
    electron = {
        2: ElectronGeometry.LINEAR,
        3: ElectronGeometry.TRIGONAL_PLANAR,
        4: ElectronGeometry.TETRAHEDRAL,
        5: ElectronGeometry.TRIGONAL_BIPYRAMIDAL,
        6: ElectronGeometry.OCTAHEDRAL,
    }.get(steric, ElectronGeometry.UNKNOWN)

    molecular = {
        (2, 0): "linear",
        (3, 0): "trigonal_planar",
        (3, 1): "bent",
        (4, 0): "tetrahedral",
        (4, 1): "trigonal_pyramidal",
        (4, 2): "bent",
        (5, 0): "trigonal_bipyramidal",
        (5, 1): "seesaw",
        (5, 2): "T_shaped",
        (5, 3): "linear",
        (6, 0): "octahedral",
        (6, 1): "square_pyramidal",
        (6, 2): "square_planar",
    }.get((steric, lone_pair_domains), "not_resolved")

    explanation = (
        "VSEPR treats electron domains as regions of electron density that repel "
        "one another; multiple bonds count as one domain for this geometry model."
    )
    return VSEPRResult(
        steric_number=steric,
        bonding_domains=bonding_domains,
        lone_pair_domains=lone_pair_domains,
        electron_geometry=electron,
        molecular_geometry=molecular,
        explanation=explanation,
    )
