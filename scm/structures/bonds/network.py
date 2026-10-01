from __future__ import annotations

from dataclasses import dataclass

from .types import BondType
from scm.structures.molecules import Molecule


@dataclass(frozen=True)
class BondNetworkSummary:
    total_bonds: int
    primary_bonds: int
    secondary_interactions: int
    bond_type_counts: tuple[tuple[str, int], ...]
    total_order_value: float


def summarize_bond_network(molecule: Molecule) -> BondNetworkSummary:
    counts: dict[str, int] = {}
    primary = 0
    secondary = 0
    order_total = 0.0

    for bond in molecule.connectivity.bonds:
        key = bond.bond_type.value
        counts[key] = counts.get(key, 0) + 1
        if bond.is_primary_bond:
            primary += 1
        else:
            secondary += 1
        if bond.order_value is not None:
            order_total += bond.order_value

    return BondNetworkSummary(
        total_bonds=len(molecule.connectivity.bonds),
        primary_bonds=primary,
        secondary_interactions=secondary,
        bond_type_counts=tuple(sorted(counts.items())),
        total_order_value=order_total,
    )
