from __future__ import annotations

from dataclasses import dataclass

from .types import BondOrder
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scm.structures.molecules import Molecule


@dataclass(frozen=True)
class ResonanceStructure:
    molecule: Molecule
    bond_orders: tuple[BondOrder, ...]

    def __post_init__(self) -> None:
        if len(self.bond_orders) != len(self.molecule.connectivity.bonds):
            raise ValueError("bond_orders must align with molecule connectivity bonds")
        normalized = tuple(
            item if isinstance(item, BondOrder) else BondOrder(item)
            for item in self.bond_orders
        )
        object.__setattr__(self, "bond_orders", normalized)

    @property
    def bond_count(self) -> int:
        return len(self.bond_orders)


@dataclass(frozen=True)
class ResonanceSet:
    structures: tuple[ResonanceStructure, ...]

    def __post_init__(self) -> None:
        structures = tuple(self.structures)
        if not structures:
            raise ValueError("at least one resonance structure is required")
        reference = structures[0].molecule
        reference_signature = _topology_signature(reference)
        for item in structures:
            if item.molecule.net_charge != reference.net_charge:
                raise ValueError("resonance structures must have the same net charge")
            if item.molecule.formula_counts != reference.formula_counts:
                raise ValueError("resonance structures must have the same elemental composition")
            if _topology_signature(item.molecule) != reference_signature:
                raise ValueError("resonance structures must preserve atom ordering and connectivity")
        object.__setattr__(self, "structures", structures)

    @property
    def count(self) -> int:
        return len(self.structures)

    def average_bond_order(self, bond_index: int) -> float:
        if not 0 <= bond_index < len(self.structures[0].bond_orders):
            raise IndexError("bond_index out of range")
        values = [
            _order_value(item.bond_orders[bond_index])
            for item in self.structures
        ]
        return sum(values) / len(values)


def _order_value(order: BondOrder) -> float:
    return {
        BondOrder.SINGLE: 1.0,
        BondOrder.DOUBLE: 2.0,
        BondOrder.TRIPLE: 3.0,
        BondOrder.QUADRUPLE: 4.0,
        BondOrder.AROMATIC: 1.5,
        BondOrder.PARTIAL: 0.5,
    }.get(order, 0.0)


def _topology_signature(molecule: Molecule) -> tuple:
    labels = tuple(item.identity_key for item in molecule.species)
    index = {id(item): i for i, item in enumerate(molecule.species)}
    edges = []
    for bond in molecule.connectivity.bonds:
        first = index[id(bond.first)]
        second = index[id(bond.second)]
        edges.append(tuple(sorted((first, second))))
    return labels, tuple(sorted(edges))
