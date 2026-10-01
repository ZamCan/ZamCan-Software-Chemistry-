from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BondFeasibility(str, Enum):
    """Evidence state for a proposed interaction."""

    PLAUSIBLE = "plausible"
    CONDITION_DEPENDENT = "condition_dependent"
    INSUFFICIENT_DATA = "insufficient_data"
    CONTRADICTED = "contradicted"


@dataclass(frozen=True)
@dataclass(frozen=True)
class BondPhysics:
    """Compact mathematical model inventory for bonding analysis."""
    coulomb_energy: str
    quantum_basis: str
    electrostatic_force: str
    bond_order_model: str
    caveat: str


@dataclass(frozen=True)
class BondTheory:
    """Scientific explanation attached to a bond classification.

    The equations are conceptual models used by the SCM reasoning layer:
    electrostatic interaction follows Coulomb's law, while covalent bonding
    is treated through electron sharing/overlap and quantum-mechanical
    electronic structure. Numerical energy or feasibility claims require
    appropriate input data rather than a generic heuristic.
    """

    type: str
    order: str
    electron_description: str
    mathematical_basis: tuple[str, ...]
    physical_influences: tuple[str, ...]
    chemical_consequences: tuple[str, ...]


BOND_THEORIES: dict[str, BondTheory] = {
    "polar_covalent": BondTheory(
        type="polar_covalent",
        order="Covalent bond order; polarity reflects unequal electron distribution rather than a separate bond-order system.",
        electron_description="Shared electron density is shifted toward the more electronegative atom.",
        mathematical_basis=("Dipole moment is represented by μ = q r for a simple charge-separation model.", "Ionic character varies continuously with electronegativity difference; no universal hard cutoff exists."),
        physical_influences=("electronegativity difference", "bond length", "electronic structure", "environment"),
        chemical_consequences=("bond polarity", "dipole moments", "reactivity", "spectroscopic behavior"),
    ),
    "covalent": BondTheory(
        type="covalent",
        order="Bond order describes the effective number of bonding interactions; "
              "single/double/triple are structural shorthand.",
        electron_description="Electron density is shared between atoms through "
                             "overlap of atomic orbitals and formation of molecular orbitals.",
        mathematical_basis=(
            "Coulomb terms govern attraction/repulsion between charged particles.",
            "Quantum mechanics determines allowed molecular states from the electronic Hamiltonian.",
            "MO bond order can be expressed as (N_bonding - N_antibonding)/2.",
        ),
        physical_influences=(
            "orbital energy and symmetry",
            "orbital overlap",
            "internuclear distance",
            "nuclear charge and shielding",
            "electron-electron repulsion",
            "environment and solvent",
        ),
        chemical_consequences=(
            "bond length and force constant",
            "molecular geometry",
            "polarity and dipole moment",
            "reactivity and spectroscopy",
        ),
    ),
    "ionic": BondTheory(
        type="ionic",
        order="No universal integer bond order is assigned to an ion-ion electrostatic attraction.",
        electron_description="Charge-separated species attract through long-range electrostatic interaction; "
                             "many solids have substantial ionic character while retaining some covalent character.",
        mathematical_basis=(
            "Coulomb interaction: U proportional to q1*q2/r.",
            "In ionic solids, lattice energy depends on charge, separation, and crystal structure.",
            "Born-type models add short-range repulsion to electrostatic attraction.",
        ),
        physical_influences=(
            "ionic charge",
            "ionic radius",
            "dielectric environment",
            "lattice geometry",
            "polarizability",
        ),
        chemical_consequences=(
            "crystal formation",
            "melting and boiling behavior",
            "solubility and hydration",
            "electrical conductivity when molten or dissolved",
        ),
    ),
    "metallic": BondTheory(
        type="metallic",
        order="No single localized bond order generally represents metallic bonding.",
        electron_description="Valence electrons are delocalized through an extended metallic electronic structure.",
        mathematical_basis=(
            "Band/solid-state models describe allowed electronic states across a lattice.",
            "Electrostatic ion-electron and electron-electron terms contribute to cohesion.",
        ),
        physical_influences=(
            "band filling",
            "lattice structure",
            "electron density",
            "defects and temperature",
        ),
        chemical_consequences=(
            "electrical and thermal conductivity",
            "ductility and malleability",
            "reflectivity",
            "alloy behavior",
        ),
    ),
    "multicenter": BondTheory(
        type="multicenter",
        order="Bonding distributed over more than two atoms.",
        electron_description="Electron density can stabilize a group of nuclei through delocalized or three-center interactions.",
        mathematical_basis=("Requires an electronic-structure description rather than pairwise Lewis bookkeeping alone.",),
        physical_influences=("orbital symmetry", "electron count", "geometry", "charge"),
        chemical_consequences=("unusual bonding", "electron-deficient structures", "cluster and hypervalent chemistry"),
    ),
    "halogen": BondTheory(
        type="halogen",
        order="Usually treated as a noncovalent interaction rather than a conventional primary bond.",
        electron_description="An electrophilic region associated with a covalently bound halogen can interact with a donor.",
        mathematical_basis=("Electrostatics, polarization, dispersion and charge-transfer contributions may all matter.",),
        physical_influences=("halogen identity", "donor strength", "geometry", "environment"),
        chemical_consequences=("molecular recognition", "crystal packing", "supramolecular assembly"),
    ),
    "coordinate": BondTheory(
        type="coordinate",
        order="Coordinate donation describes electron-pair origin, not a fundamentally different force law.",
        electron_description="A donor supplies an electron pair to an acceptor orbital; after formation the bonding electrons are shared.",
        mathematical_basis=(
            "Lewis donor/acceptor bookkeeping identifies the electron-pair source.",
            "Molecular-orbital treatment describes the resulting bonding state.",
        ),
        physical_influences=(
            "donor lone-pair energy",
            "acceptor orbital availability",
            "orbital symmetry",
            "steric environment",
            "solvent and ligand field",
        ),
        chemical_consequences=(
            "coordination complexes",
            "Lewis acid-base chemistry",
            "catalysis",
            "biometal binding",
        ),
    ),
    "hydrogen": BondTheory(
        type="hydrogen",
        order="Usually no conventional primary bond order is assigned.",
        electron_description="A hydrogen atom covalently bound to an electronegative donor interacts with an acceptor lone pair or electron density.",
        mathematical_basis=(
            "Electrostatic attraction is important.",
            "Dispersion, polarization, charge transfer, and orbital interactions can contribute.",
            "Strength depends strongly on geometry and environment.",
        ),
        physical_influences=(
            "donor/acceptor electronegativity",
            "H···acceptor distance",
            "directionality",
            "solvent",
            "temperature",
        ),
        chemical_consequences=(
            "water structure",
            "protein and nucleic-acid architecture",
            "crystal packing",
            "boiling and melting behavior",
        ),
    ),
    "van_der_waals": BondTheory(
        type="van_der_waals",
        order="No conventional bond order.",
        electron_description="Weak intermolecular attraction arises from instantaneous and induced charge distributions and, depending on the system, permanent multipoles.",
        mathematical_basis=(
            "Dispersion attraction is commonly represented by inverse-power terms such as -C6/r^6.",
            "Repulsion at short range prevents collapse.",
        ),
        physical_influences=(
            "polarizability",
            "distance",
            "molecular surface",
            "temperature",
            "environment",
        ),
        chemical_consequences=(
            "condensation",
            "molecular packing",
            "adsorption",
            "material and biomolecular recognition",
        ),
    ),
}


def get_bond_theory(bond_type: str) -> BondTheory:
    key = bond_type.strip().casefold()
    try:
        return BOND_THEORIES[key]
    except KeyError as exc:
        raise ValueError(f"unknown bond type: {bond_type!r}") from exc


BOND_PHYSICS = BondPhysics(
    coulomb_energy="U(r) = k_e q1 q2 / r for point-charge electrostatics.",
    quantum_basis="Electronic states follow the quantum Hamiltonian; bonding is associated with a lower-energy electronic state than separated constituents when a stable minimum exists.",
    electrostatic_force="F(r) = k_e q1 q2 / r^2 for the point-charge component.",
    bond_order_model="MO bond order = (N_bonding - N_antibonding) / 2; localized Lewis bond order counts shared electron pairs.",
    caveat="These are models, not a universal single equation for every bond. Real systems require geometry, electron density, quantum state, environment and, where needed, experimental evidence.",
)


def classify_covalent_character(electronegativity_difference: float) -> str:
    """Describe polarity without pretending a hard ionic/covalent boundary exists."""
    if electronegativity_difference < 0:
        raise ValueError("electronegativity difference must be nonnegative")
    if electronegativity_difference == 0:
        return "nonpolar_covalent"
    return "polar_covalent"


def bond_order_consequence(order: BondOrder) -> tuple[str, ...]:
    """Return qualitative consequences, not fabricated numerical properties."""
    return {
        BondOrder.SINGLE: ("one formal bonding pair", "often longer/weaker than higher-order bonds of the same atom pair"),
        BondOrder.DOUBLE: ("two formal bonding pairs", "often shorter/stronger than the corresponding single bond"),
        BondOrder.TRIPLE: ("three formal bonding pairs", "often shorter/stronger than the corresponding double bond"),
        BondOrder.QUADRUPLE: ("four formal bonding interactions in systems where supported", "requires appropriate electronic structure"),
        BondOrder.AROMATIC: ("delocalized bonding representation", "individual bonds need not have integer localized order"),
        BondOrder.PARTIAL: ("fractional/effective bonding character", "common in delocalized or averaged descriptions"),
        BondOrder.UNKNOWN: ("bond order not established",),
    }[order]
