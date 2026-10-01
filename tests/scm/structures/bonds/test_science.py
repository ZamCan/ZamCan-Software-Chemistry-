from scm.structures.bonds import (
    BondFeasibility,
    BondOrder,
    BondType,
    assess_bond_proposal,
    get_bond_theory,
)


def test_bond_order_is_distinct_from_bond_type():
    assert BondOrder.DOUBLE.value == "double"
    assert BondType.COVALENT.value == "covalent"


def test_ionic_bond_has_no_forced_integer_bond_order():
    theory = get_bond_theory("ionic")
    assert "No universal integer bond order" in theory.order


def test_covalent_theory_contains_molecular_orbital_bond_order():
    theory = get_bond_theory("covalent")
    assert any("N_bonding" in item for item in theory.mathematical_basis)


def test_missing_evidence_does_not_become_a_false_bond_prediction():
    result = assess_bond_proposal(
        bond_type=BondType.COVALENT,
        order=BondOrder.SINGLE,
    )
    assert result.feasibility is BondFeasibility.INSUFFICIENT_DATA
    assert result.missing_data


def test_coordinate_bond_requires_donor_electron_pair():
    result = assess_bond_proposal(
        bond_type=BondType.COORDINATE,
        order=BondOrder.SINGLE,
        donor_electron_pair=False,
    )
    assert result.feasibility is BondFeasibility.CONTRADICTED
