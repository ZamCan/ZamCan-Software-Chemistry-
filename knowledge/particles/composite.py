from __future__ import annotations

from fractions import Fraction

from scm.core import Quantity
from scm.matter.particles import (
    Particle,
    ParticleDomain,
    ParticleFamily,
    ParticleRole,
    Spin,
)


proton = Particle(
    name="proton",
    symbol="p",
    rest_mass=Quantity(1.67262192595e-27, "kg"),
    elementary_charge_number=1,
    intrinsic_spin=Spin(Fraction(1, 2)),
    domain=ParticleDomain.COMPOSITE,
    family=ParticleFamily.BARYON,
    roles=frozenset({
        ParticleRole.NUCLEON,
    }),
)


neutron = Particle(
    name="neutron",
    symbol="n",
    rest_mass=Quantity(1.67492750056e-27, "kg"),
    elementary_charge_number=0,
    intrinsic_spin=Spin(Fraction(1, 2)),
    domain=ParticleDomain.COMPOSITE,
    family=ParticleFamily.BARYON,
    roles=frozenset({
        ParticleRole.NUCLEON,
    }),
)


__all__ = [
    "proton",
    "neutron",
]
