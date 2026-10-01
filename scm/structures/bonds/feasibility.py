from __future__ import annotations

from dataclasses import dataclass

from .analysis import BondFeasibility
from .types import BondOrder, BondType


@dataclass(frozen=True)
class BondProposal:
    """Explainable proposal before a Bond object is accepted as structure."""

    bond_type: BondType
    order: BondOrder
    feasibility: BondFeasibility
    reasons: tuple[str, ...]
    missing_data: tuple[str, ...] = ()


def assess_bond_proposal(
    *,
    bond_type: BondType,
    order: BondOrder,
    donor_electron_pair: bool | None = None,
    electrostatic_pairing: bool | None = None,
    metallic_lattice: bool | None = None,
    hydrogen_donor_acceptor_geometry: bool | None = None,
    orbital_compatibility: bool | None = None,
) -> BondProposal:
    """Classify only from supplied evidence; never invent missing chemistry.

    This is deliberately an evidence gate, not a universal bond-prediction
    algorithm. A future electronic-structure engine can replace the inputs
    with computed orbital, energetic, geometric and environmental evidence.
    """

    reasons: list[str] = []
    missing: list[str] = []

    if bond_type is BondType.COORDINATE:
        if donor_electron_pair is False:
            return BondProposal(
                bond_type, order, BondFeasibility.CONTRADICTED,
                ("Coordinate bonding requires a donor electron pair.",),
            )
        if donor_electron_pair is None:
            missing.append("donor electron-pair availability")

    elif bond_type is BondType.IONIC:
        if electrostatic_pairing is False:
            return BondProposal(
                bond_type, order, BondFeasibility.CONTRADICTED,
                ("The supplied evidence does not support the required electrostatic charge interaction.",),
            )
        if electrostatic_pairing is None:
            missing.append("charge distribution and electrostatic evidence")

    elif bond_type is BondType.METALLIC:
        if metallic_lattice is False:
            return BondProposal(
                bond_type, order, BondFeasibility.CONTRADICTED,
                ("A metallic bond model requires an appropriate extended metallic electronic/lattice system.",),
            )
        if metallic_lattice is None:
            missing.append("metallic lattice/electronic-state evidence")

    elif bond_type is BondType.HYDROGEN:
        if hydrogen_donor_acceptor_geometry is False:
            return BondProposal(
                bond_type, order, BondFeasibility.CONTRADICTED,
                ("Hydrogen bonding requires a chemically appropriate donor/acceptor relationship and geometry.",),
            )
        if hydrogen_donor_acceptor_geometry is None:
            missing.append("hydrogen-bond donor/acceptor and geometry")

    elif bond_type is BondType.COVALENT:
        if orbital_compatibility is False:
            return BondProposal(
                bond_type, order, BondFeasibility.CONTRADICTED,
                ("The supplied evidence does not support compatible orbital/electronic overlap.",),
            )
        if orbital_compatibility is None:
            missing.append("orbital compatibility and electronic-state evidence")

    if missing:
        return BondProposal(
            bond_type,
            order,
            BondFeasibility.INSUFFICIENT_DATA,
            tuple(reasons) or ("The proposed bond type is not established by the supplied evidence.",),
            tuple(missing),
        )

    reasons.append("The supplied evidence is compatible with the selected bonding model.")
    return BondProposal(
        bond_type,
        order,
        BondFeasibility.PLAUSIBLE,
        tuple(reasons),
    )
