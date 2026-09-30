from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ElectronSpin(str, Enum):
    """
    Intrinsic spin projection of an electron along a chosen quantization axis.

    The two allowed projections are:
        +1/2
        -1/2
    """

    UP = "up"
    DOWN = "down"

    @property
    def quantum_number(self) -> float:
        return 0.5 if self is ElectronSpin.UP else -0.5


@dataclass(frozen=True)
class OrbitalElectron:
    """
    One electron assigned to an atomic orbital.

    Spin is explicitly represented so that Pauli exclusion and
    Hund-type occupancy rules can be modeled structurally.
    """

    spin: ElectronSpin

    def __post_init__(self) -> None:
        if not isinstance(self.spin, ElectronSpin):
            raise TypeError("spin must be an ElectronSpin")

    @property
    def spin_quantum_number(self) -> float:
        return self.spin.quantum_number
