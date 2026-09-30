from __future__ import annotations

from scm.core import Quantity


# =============================================================================
# ELECTROMAGNETIC CONSTANTS
# =============================================================================

# Elementary charge.
#
# Exact SI value:
# e = 1.602176634 × 10^-19 C
#
# Exact by definition in the SI.
e = Quantity(1.602176634e-19, "C")


# =============================================================================
# QUANTUM PHYSICAL CONSTANTS
# =============================================================================

# Reduced Planck constant.
#
# ħ ≈ 1.054571817 × 10^-34 J·s
#
# SI dimension:
# J·s = kg·m²·s⁻¹
#
# This is the reduced Planck constant used in quantum mechanics.
hbar = Quantity(1.054571817e-34, "J·s")


# =============================================================================
# AMOUNT OF SUBSTANCE
# =============================================================================

# Avogadro constant.
#
# Exact SI value:
# N_A = 6.02214076 × 10^23 mol⁻¹
#
# This connects amount of substance with the number of specified entities.
N_A = Quantity(6.02214076e23, "mol⁻¹")


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    "e",
    "hbar",
    "N_A",
]
