from scm.structures.bonds import (
    BondComponent,
    BondOrder,
    BondType,
    explain_bond_possibility,
    get_valence_profile,
    valence_electron_count,
)
from scm.structures.bonds.analysis import BOND_PHYSICS, classify_covalent_character


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
