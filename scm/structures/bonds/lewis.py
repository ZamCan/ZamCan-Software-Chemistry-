from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from scm.matter.atoms import Atom
from scm.structures.bonds import Bond, BondOrder, BondType
from scm.structures.molecules import Molecule


class OctetStatus(str, Enum):
    DUET = "duet"
    OCTET = "octet"
    EXPANDED = "expanded"
    DEFICIENT = "deficient"
    ODD_ELECTRON = "odd_electron"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class LewisAtomBookkeeping:
    atom: Atom
    valence_electrons: int
    nonbonding_electrons: int
    bonding_order_sum: float
    electrons_around_atom: float
    formal_charge: float
    target_electrons: int | None
    status: OctetStatus


@dataclass(frozen=True)
class LewisBookkeeping:
    molecule: Molecule
    total_valence_electrons: int
    assigned_bonding_electrons: float
    assigned_nonbonding_electrons: int
    atoms: tuple[LewisAtomBookkeeping, ...]

    @property
    def formal_charge_sum(self) -> float:
        return sum(item.formal_charge for item in self.atoms)

    @property
    def electron_accounted_for(self) -> float:
        return self.assigned_bonding_electrons + self.assigned_nonbonding_electrons


def _bond_order_value(bond: Bond) -> float:
    values = {
        BondOrder.SINGLE: 1.0,
        BondOrder.DOUBLE: 2.0,
        BondOrder.TRIPLE: 3.0,
        BondOrder.QUADRUPLE: 4.0,
        BondOrder.AROMATIC: 1.5,
        BondOrder.PARTIAL: 0.5,
    }
    return values.get(bond.order, 0.0)


def _is_primary_electron_pair_bond(bond: Bond) -> bool:
    return bond.bond_type in {
        BondType.COVALENT,
        BondType.POLAR_COVALENT,
        BondType.COORDINATE,
        BondType.MULTICENTER,
    }


def target_electron_count(atom: Atom) -> tuple[int | None, OctetStatus]:
    z = atom.atomic_number
    if z in (1, 2):
        return 2, OctetStatus.DUET
    if 3 <= z <= 20:
        return 8, OctetStatus.OCTET
    # The simple octet target is not a universal rule for heavier atoms.
    return 8, OctetStatus.OCTET


def build_lewis_bookkeeping(
    molecule: Molecule,
    lone_pairs: tuple[int, ...],
) -> LewisBookkeeping:
    """Audit a supplied Lewis structure without inventing lone-pair placement.

    lone_pairs is aligned with molecule.species. Every species must be an Atom;
    structural bond information supplies the bonding-order contribution.
    """
    if len(lone_pairs) != len(molecule.species):
        raise ValueError("lone_pairs must contain one entry per molecule species")
    if any(isinstance(value, bool) or value < 0 for value in lone_pairs):
        raise ValueError("lone-pair counts must be nonnegative integers")

    atoms = tuple(molecule.species)
    if any(not isinstance(item, Atom) for item in atoms):
        raise TypeError("Lewis bookkeeping currently requires atom-level molecules")

    total_valence = sum(item.valence_electron_count for item in atoms) - molecule.net_charge

    bonding_electrons = 0.0
    for bond in molecule.connectivity.bonds:
        if _is_primary_electron_pair_bond(bond):
            bonding_electrons += 2.0 * _bond_order_value(bond)

    nonbonding_electrons = 2 * sum(lone_pairs)
    records: list[LewisAtomBookkeeping] = []

    for index, atom in enumerate(atoms):
        bond_sum = sum(
            _bond_order_value(bond)
            for bond in molecule.bonds_for(atom)
            if _is_primary_electron_pair_bond(bond)
        )
        nonbonding = 2 * lone_pairs[index]
        around = nonbonding + 2.0 * bond_sum
        formal_charge = atom.valence_electron_count - nonbonding - bond_sum
        target, status = target_electron_count(atom)

        if target is not None:
            if around < target:
                status = OctetStatus.DEFICIENT if around % 2 == 0 else OctetStatus.ODD_ELECTRON
            elif around > target:
                status = OctetStatus.EXPANDED
            else:
                status = OctetStatus.DUET if target == 2 else OctetStatus.OCTET

        records.append(
            LewisAtomBookkeeping(
                atom=atom,
                valence_electrons=atom.valence_electron_count,
                nonbonding_electrons=nonbonding,
                bonding_order_sum=bond_sum,
                electrons_around_atom=around,
                formal_charge=formal_charge,
                target_electrons=target,
                status=status,
            )
        )

    return LewisBookkeeping(
        molecule=molecule,
        total_valence_electrons=total_valence,
        assigned_bonding_electrons=bonding_electrons,
        assigned_nonbonding_electrons=nonbonding_electrons,
        atoms=tuple(records),
    )
