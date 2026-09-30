from __future__ import annotations

from enum import Enum
from fractions import Fraction


class ParticleDomain(str, Enum):
    ELEMENTARY = "elementary"
    COMPOSITE = "composite"


class ParticleFamily(str, Enum):
    LEPTON = "lepton"
    QUARK = "quark"
    GAUGE_BOSON = "gauge_boson"
    HIGGS_BOSON = "higgs_boson"
    BARYON = "baryon"
    MESON = "meson"


class ParticleRole(str, Enum):
    """
    Functional or structural classifications that can apply
    across the particle-family taxonomy.

    A role is not a particle family.
    """

    NUCLEON = "nucleon"


class ParticleStatistics(str, Enum):
    BOSONIC = "bosonic"
    FERMIONIC = "fermionic"


_ELEMENTARY_FAMILIES = frozenset({
    ParticleFamily.LEPTON,
    ParticleFamily.QUARK,
    ParticleFamily.GAUGE_BOSON,
    ParticleFamily.HIGGS_BOSON,
})

_COMPOSITE_FAMILIES = frozenset({
    ParticleFamily.BARYON,
    ParticleFamily.MESON,
})


def validate_particle_taxonomy(
    domain: ParticleDomain,
    family: ParticleFamily,
) -> None:
    if not isinstance(domain, ParticleDomain):
        raise TypeError("domain must be a ParticleDomain")

    if not isinstance(family, ParticleFamily):
        raise TypeError("family must be a ParticleFamily")

    if domain is ParticleDomain.ELEMENTARY:
        if family not in _ELEMENTARY_FAMILIES:
            raise ValueError(
                f"{family.value} is not an elementary particle family"
            )

    elif domain is ParticleDomain.COMPOSITE:
        if family not in _COMPOSITE_FAMILIES:
            raise ValueError(
                f"{family.value} is not a composite particle family"
            )


def validate_particle_role(
    role: ParticleRole,
    domain: ParticleDomain,
    family: ParticleFamily,
) -> None:
    if not isinstance(role, ParticleRole):
        raise TypeError("role must be a ParticleRole")

    if role is ParticleRole.NUCLEON:
        if domain is not ParticleDomain.COMPOSITE:
            raise ValueError(
                "nucleon role requires a composite particle"
            )

        if family is not ParticleFamily.BARYON:
            raise ValueError(
                "nucleon role requires the baryon family"
            )


def statistics_from_spin(
    quantum_number: Fraction,
) -> ParticleStatistics:
    if not isinstance(quantum_number, Fraction):
        raise TypeError(
            "spin quantum number must be a Fraction"
        )

    if quantum_number < 0:
        raise ValueError(
            "spin quantum number must be non-negative"
        )

    doubled_spin = 2 * quantum_number

    if doubled_spin.denominator != 1:
        raise ValueError(
            "spin quantum number must be an integer or half-integer"
        )

    if doubled_spin.numerator % 2 == 0:
        return ParticleStatistics.BOSONIC

    return ParticleStatistics.FERMIONIC
