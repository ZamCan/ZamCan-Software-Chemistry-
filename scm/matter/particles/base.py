from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from scm.core import Quantity
from knowledge.constants.physical import e

from .spin import Spin
from .taxonomy import (
    ParticleDomain,
    ParticleFamily,
    ParticleRole,
    ParticleStatistics,
    statistics_from_spin,
    validate_particle_role,
    validate_particle_taxonomy,
)


@dataclass(frozen=True)
class Particle:
    name: str
    symbol: str
    rest_mass: Quantity
    elementary_charge_number: int
    intrinsic_spin: Optional[Spin] = None
    domain: Optional[ParticleDomain] = None
    family: Optional[ParticleFamily] = None
    roles: frozenset[ParticleRole] = frozenset()

    def __post_init__(self) -> None:
        if self.domain is None and self.family is None:
            if self.roles:
                raise ValueError(
                    "roles require domain and family to be provided"
                )
            return

        if self.domain is None or self.family is None:
            raise ValueError(
                "domain and family must either both be provided or both be omitted"
            )

        validate_particle_taxonomy(
            self.domain,
            self.family,
        )

        for role in self.roles:
            validate_particle_role(
                role,
                self.domain,
                self.family,
            )

    @property
    def electric_charge(self) -> Quantity:
        return self.elementary_charge_number * e

    @property
    def charge_symbol(self) -> str:
        if self.elementary_charge_number == 0:
            return "0"

        if self.elementary_charge_number == 1:
            return "+e"

        if self.elementary_charge_number == -1:
            return "-e"

        return f"{self.elementary_charge_number:+d}e"

    @property
    def statistics(self) -> Optional[ParticleStatistics]:
        if self.intrinsic_spin is None:
            return None

        return statistics_from_spin(
            self.intrinsic_spin.quantum_number
        )

    @property
    def is_nucleon(self) -> bool:
        return ParticleRole.NUCLEON in self.roles

    def __str__(self) -> str:
        return self.symbol
