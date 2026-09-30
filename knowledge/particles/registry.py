from __future__ import annotations

from typing import Dict

from scm.matter.particles import Particle

from .composite import neutron, proton
from .elementary import electron, photon


_PARTICLES: Dict[str, Particle] = {
    # Electron
    "electron": electron,
    "e⁻": electron,
    "e-": electron,

    # Photon
    "photon": photon,
    "γ": photon,

    # Proton
    "proton": proton,
    "p": proton,

    # Neutron
    "neutron": neutron,
    "n": neutron,
}


def get_particle(identifier: str) -> Particle:
    """
    Retrieve a known particle by name, symbol, or registered alias.

    Raises:
        TypeError:
            If identifier is not a string.

        KeyError:
            If the particle is not registered.
    """
    if not isinstance(identifier, str):
        raise TypeError(
            "particle identifier must be a string"
        )

    key = identifier.strip()

    try:
        return _PARTICLES[key]
    except KeyError as exc:
        raise KeyError(
            f"Unknown particle: {identifier!r}"
        ) from exc


def all_particles() -> tuple[Particle, ...]:
    """
    Return all unique particles known to the registry.
    """
    return tuple(
        dict.fromkeys(_PARTICLES.values())
    )


__all__ = [
    "get_particle",
    "all_particles",
]
