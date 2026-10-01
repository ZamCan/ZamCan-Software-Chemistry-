from scm.structures.bonds import (
    BondComponent,
    BondOrder,
    BondType,
    explain_bond_possibility,
    get_valence_profile,
    valence_electron_count,
)
from scm.structures.bonds.analysis import BOND_PHYSICS, classify_covalent_character
from scm.structures.connectivity import Connectivity
from scm.structures.molecules import Molecule
from scm.matter.atoms import Atom



def test_bond_taxonomy_contains_real_chemical_regimes():
    assert BondType.POLAR_COVALENT.value == "polar_covalent"
    assert BondType.MULTICENTER.value == "multicenter"
    assert BondType.HALOGEN.value == "halogen"
    assert BondComponent.SIGMA.value == "sigma"
    assert BondComponent.PI.value == "pi"


def test_bond_physics_keeps_electrostatics_and_quantum_models_distinct():
    assert "q1 q2" in BOND_PHYSICS.coulomb_energy
    assert "quantum" in BOND_PHYSICS.quantum_basis.lower()
    assert "N_bonding" in BOND_PHYSICS.bond_order_model


def test_common_valence_is_not_treated_as_universal():
    carbon = get_valence_profile("C")
    assert carbon is not None
    assert carbon.common_valences == (4,)
    assert valence_electron_count("C") == 4


def test_bond_screening_reports_missing_deep_evidence():
    reasons = explain_bond_possibility("C", "O", proposed_order=2)
    assert any("orbital" in item.lower() for item in reasons)


def test_electronegativity_difference_changes_polarity_description():
    assert classify_covalent_character(0.0) == "nonpolar_covalent"
    assert classify_covalent_character(1.0) == "polar_covalent"


def test_energy_curve_analysis_finds_supplied_equilibrium_minimum():
    from scm.structures.bonds import BondEnergyPoint, assess_energy_curve

    result = assess_energy_curve((
        BondEnergyPoint(0.8, 2.0),
        BondEnergyPoint(1.0, -1.0),
        BondEnergyPoint(1.2, 1.0),
    ))

    assert result.stable_minimum
    assert result.equilibrium_distance == 1.0
    assert result.minimum_energy == -1.0


def test_coulomb_energy_has_expected_sign():
    from scm.structures.bonds import coulomb_energy

    assert coulomb_energy(1.0, -1.0, 2.0, 1.0) < 0
    assert coulomb_energy(1.0, 1.0, 2.0, 1.0) > 0


def test_water_lewis_bookkeeping_conserves_electrons_and_formal_charge():
    from scm.structures.bonds import build_lewis_bookkeeping

    o = Atom.create(8)
    h1 = Atom.create(1)
    h2 = Atom.create(1)
    molecule = Molecule(
        species=(o, h1, h2),
        connectivity=Connectivity(
            nodes=(o, h1, h2),
            bonds=(Bond(o, h1), Bond(o, h2)),
        ),
        charge=0,
    )

    result = build_lewis_bookkeeping(molecule, (2, 0, 0))

    assert result.total_valence_electrons == 8
    assert result.electron_accounted_for == 8.0
    assert result.formal_charge_sum == 0
    assert result.atoms[0].status.value == "octet"
    assert all(item.formal_charge == 0 for item in result.atoms)


def test_carbon_dioxide_double_bonds_have_sixteen_accounted_electrons():
    from scm.structures.bonds import build_lewis_bookkeeping

    c = Atom.create(6)
    o1 = Atom.create(8)
    o2 = Atom.create(8)
    molecule = Molecule(
        species=(c, o1, o2),
        connectivity=Connectivity(
            nodes=(c, o1, o2),
            bonds=(
                Bond(c, o1, BondOrder.DOUBLE),
                Bond(c, o2, BondOrder.DOUBLE),
            ),
        ),
        charge=0,
    )

    result = build_lewis_bookkeeping(molecule, (0, 2, 2))

    assert result.total_valence_electrons == 16
    assert result.electron_accounted_for == 16.0
    assert all(item.formal_charge == 0 for item in result.atoms)


def test_vsepr_maps_common_domain_patterns():
    from scm.structures.bonds import analyze_vsepr

    assert analyze_vsepr(2, 0).molecular_geometry == "linear"
    assert analyze_vsepr(3, 0).molecular_geometry == "trigonal_planar"
    assert analyze_vsepr(4, 0).molecular_geometry == "tetrahedral"
    assert analyze_vsepr(4, 1).molecular_geometry == "trigonal_pyramidal"
    assert analyze_vsepr(4, 2).molecular_geometry == "bent"


def test_resonance_set_preserves_composition_and_averages_orders():
    from scm.structures.bonds import ResonanceSet, ResonanceStructure

    n = Atom.create(7)
    o1 = Atom.create(8)
    o2 = Atom.create(8)
    molecule = Molecule(
        species=(n, o1, o2),
        connectivity=Connectivity(
            nodes=(n, o1, o2),
            bonds=(Bond(n, o1), Bond(n, o2)),
        ),
        charge=0,
    )
    first = ResonanceStructure(molecule, (BondOrder.DOUBLE, BondOrder.SINGLE))
    second = ResonanceStructure(molecule, (BondOrder.SINGLE, BondOrder.DOUBLE))
    resonance = ResonanceSet((first, second))

    assert resonance.count == 2
    assert resonance.average_bond_order(0) == 1.5
    assert resonance.average_bond_order(1) == 1.5


def test_bond_network_summary_separates_primary_and_secondary_interactions():
    from scm.structures.bonds import BondNetworkSummary, summarize_bond_network

    o = Atom.create(8)
    h = Atom.create(1)
    c = Atom.create(6)
    graph = Connectivity(
        nodes=(o, h, c),
        bonds=(
            Bond(o, h, bond_type=BondType.COVALENT),
            Bond(o, c, bond_type=BondType.HYDROGEN),
        ),
    )
    molecule = Molecule(species=(o, h, c), connectivity=graph)

    result = summarize_bond_network(molecule)

    assert isinstance(result, BondNetworkSummary)
    assert result.primary_bonds == 1
    assert result.secondary_interactions == 1
    assert result.total_bonds == 2
