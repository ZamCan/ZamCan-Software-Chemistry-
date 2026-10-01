from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class BondEnergyPoint:
    distance: float
    energy: float


@dataclass(frozen=True)
class BondStabilityAssessment:
    stable_minimum: bool
    equilibrium_distance: float | None
    minimum_energy: float | None
    reason: str


def assess_energy_curve(points: tuple[BondEnergyPoint, ...]) -> BondStabilityAssessment:
    """Find a sampled local energy minimum without inventing an energy model.

    The caller supplies energies from an experiment, quantum calculation, or
    another validated model. This function only analyzes those values.
    """
    if len(points) < 3:
        raise ValueError("at least three energy points are required")

    ordered = tuple(sorted(points, key=lambda p: p.distance))
    if any(
        not isfinite(p.distance) or not isfinite(p.energy)
        for p in ordered
    ):
        raise ValueError("distance and energy must be finite")

    for left, right in zip(ordered, ordered[1:]):
        if left.distance == right.distance:
            raise ValueError("distances must be unique")

    minima = [
        ordered[i]
        for i in range(1, len(ordered) - 1)
        if ordered[i].energy < ordered[i - 1].energy
        and ordered[i].energy < ordered[i + 1].energy
    ]

    if not minima:
        return BondStabilityAssessment(
            stable_minimum=False,
            equilibrium_distance=None,
            minimum_energy=None,
            reason="The supplied sampled energy curve contains no interior local minimum; bonding stability is not established by these samples.",
        )

    minimum = min(minima, key=lambda p: p.energy)
    return BondStabilityAssessment(
        stable_minimum=True,
        equilibrium_distance=minimum.distance,
        minimum_energy=minimum.energy,
        reason="The supplied energy curve contains a local minimum, providing evidence for a stable configuration within the sampled model.",
    )


def coulomb_energy(q1: float, q2: float, distance: float, k_e: float) -> float:
    """Point-charge electrostatic potential energy."""
    if distance <= 0:
        raise ValueError("distance must be positive")
    return k_e * q1 * q2 / distance
