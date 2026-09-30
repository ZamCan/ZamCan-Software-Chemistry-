from __future__ import annotations

from fractions import Fraction

from scm.core import Quantity
from scm.matter.particles import (
    Particle,
    ParticleDomain,
    ParticleFamily,
    Spin,
)


# =============================================================================
# ELECTRON
# =============================================================================

electron = Particle(
    name="electron",
    symbol="e⁻",
    rest_mass=Quantity(
        9.1093837139e-31,
        "kg",
    ),
    elementary_charge_number=-1,
    intrinsic_spin=Spin(Fraction(1, 2)),
    domain=ParticleDomain.ELEMENTARY,
    family=ParticleFamily.LEPTON,
)


# =============================================================================
# PHOTON
# =============================================================================

photon = Particle(
    name="photon",
    symbol="γ",
    rest_mass=Quantity(
        0.0,
        "kg",
    ),
    elementary_charge_number=0,
    intrinsic_spin=Spin(Fraction(1)),
    domain=ParticleDomain.ELEMENTARY,
    family=ParticleFamily.GAUGE_BOSON,
)


__all__ = [
    "electron",
    "photon",
]
