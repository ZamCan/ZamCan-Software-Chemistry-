import pytest

from scm.chemistry.amount import AmountOfSubstance
from scm.core import Conditions, Phase, Quantity, ScientificStatus
from scm.matter.atoms import Atom
from scm.matter.states import ChemicalState, StateComponent


def make_hydrogen_component(moles: float = 2.0) -> StateComponent:
    hydrogen = Atom.create(1)

    amount = AmountOfSubstance(
        Quantity(moles, "mol"),
        "hydrogen atoms",
    )

    return StateComponent(
        species=hydrogen,
        amount=amount,
    )


def test_state_component_connects_species_and_amount():
    component = make_hydrogen_component(2.0)

    assert component.species.atomic_number == 1
    assert component.moles == 2.0
    assert component.quantity.to("mol").value == 2.0
    assert component.entity == "hydrogen atoms"


def test_state_component_rejects_invalid_species():
    with pytest.raises(TypeError):
        StateComponent(
            species="H",
            amount=AmountOfSubstance(
                Quantity(1.0, "mol"),
                "hydrogen",
            ),
        )


def test_state_component_rejects_invalid_amount():
    hydrogen = Atom.create(1)

    with pytest.raises(TypeError):
        StateComponent(
            species=hydrogen,
            amount="1 mol",
        )


def test_chemical_state_requires_component():
    with pytest.raises(ValueError):
        ChemicalState(components=())


def test_chemical_state_rejects_invalid_component():
    with pytest.raises(TypeError):
        ChemicalState(
            components=("not a component",),
        )


def test_chemical_state_stores_components_and_species():
    component = make_hydrogen_component(2.0)

    state = ChemicalState(
        components=(component,),
        phase=Phase.GAS,
    )

    assert state.component_count == 1
    assert state.components == (component,)
    assert state.species == (component.species,)
    assert state.phase is Phase.GAS
    assert state.total_moles == 2.0


def test_chemical_state_supports_conditions_and_status():
    component = make_hydrogen_component()

    conditions = Conditions(
        temperature=Quantity(298.15, "K"),
        pressure=Quantity(101325.0, "Pa"),
    )

    state = ChemicalState(
        components=(component,),
        phase=Phase.GAS,
        conditions=conditions,
        status=ScientificStatus.OBSERVED,
    )

    assert state.conditions == conditions
    assert state.status is ScientificStatus.OBSERVED


def test_chemical_state_from_components():
    component = make_hydrogen_component(3.0)

    state = ChemicalState.from_components(
        [component],
        phase=Phase.GAS,
    )

    assert state.component_count == 1
    assert state.total_moles == 3.0


def test_chemical_state_contains_uses_species_identity():
    component = make_hydrogen_component()
    state = ChemicalState(components=(component,))

    assert state.contains(component.species)

    equivalent_but_distinct = Atom.create(1)

    assert equivalent_but_distinct is not component.species
    assert not state.contains(equivalent_but_distinct)


def test_chemical_state_components_for():
    component = make_hydrogen_component()
    state = ChemicalState(components=(component,))

    assert state.components_for(component.species) == (component,)


def test_chemical_state_property_lookup():
    component = make_hydrogen_component()

    state = ChemicalState(
        components=(component,),
    )

    assert state.property("density") is None


def test_chemical_state_normalizes_iterables():
    component = make_hydrogen_component()

    state = ChemicalState(
        components=[component],
    )

    assert isinstance(state.components, tuple)
    assert isinstance(state.properties, tuple)


def test_chemical_state_normalizes_single_evidence():
    from scm.core import Evidence, EvidenceType

    component = make_hydrogen_component()

    evidence = Evidence(
        evidence_type=EvidenceType.EXPERIMENTAL,
        source="test",
    )

    state = ChemicalState(
        components=(component,),
        evidence=evidence,
    )

    assert state.evidence == (evidence,)


def test_chemical_state_normalizes_multiple_evidence():
    from scm.core import Evidence, EvidenceType

    component = make_hydrogen_component()

    evidence = (
        Evidence(
            evidence_type=EvidenceType.EXPERIMENTAL,
            source="experiment",
        ),
        Evidence(
            evidence_type=EvidenceType.REFERENCE,
            source="reference",
        ),
    )

    state = ChemicalState(
        components=(component,),
        evidence=evidence,
    )

    assert state.evidence == evidence


def test_chemical_state_rejects_invalid_evidence():
    component = make_hydrogen_component()

    with pytest.raises(TypeError):
        ChemicalState(
            components=(component,),
            evidence="not evidence",
        )
