import pytest

from scm.chemistry.amount import AmountOfSubstance
from scm.chemistry.engine.state_resolver import ResolvedState, StateResolver
from scm.core import Quantity
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies
from scm.matter.states import ChemicalState, StateComponent


def make_hydrogen_component(moles: float = 2.0) -> StateComponent:
    hydrogen = ChemicalSpecies(
        composition=Composition.from_mapping({"H": 1})
    )
    amount = AmountOfSubstance(
        quantity=Quantity(moles, "mol"),
        entity="H",
    )
    return StateComponent(
        species=hydrogen,
        amount=amount,
    )


def make_oxygen_component(moles: float = 1.0) -> StateComponent:
    oxygen = ChemicalSpecies(
        composition=Composition.from_mapping({"O": 1})
    )
    amount = AmountOfSubstance(
        quantity=Quantity(moles, "mol"),
        entity="O",
    )
    return StateComponent(
        species=oxygen,
        amount=amount,
    )


def test_resolver_returns_resolved_state():
    component = make_hydrogen_component()
    state = ChemicalState(components=(component,))

    resolved = StateResolver.resolve(state)

    assert isinstance(resolved, ResolvedState)
    assert resolved.state is state


def test_resolver_preserves_species_identity():
    component = make_hydrogen_component()
    state = ChemicalState(components=(component,))

    resolved = StateResolver.resolve(state)

    assert resolved.species[0] is component.species


def test_resolver_reports_component_count():
    state = ChemicalState(
        components=(
            make_hydrogen_component(),
            make_oxygen_component(),
        )
    )

    resolved = StateResolver.resolve(state)

    assert resolved.component_count == 2


def test_resolver_reports_total_moles():
    state = ChemicalState(
        components=(
            make_hydrogen_component(2.0),
            make_oxygen_component(1.0),
        )
    )

    resolved = StateResolver.resolve(state)

    assert resolved.total_moles == pytest.approx(3.0)


def test_resolver_collects_element_counts():
    state = ChemicalState(
        components=(
            make_hydrogen_component(),
            make_oxygen_component(),
        )
    )

    resolved = StateResolver.resolve(state)

    assert resolved.element_counts == {
        "H": 1,
        "O": 1,
    }


def test_resolver_reports_moles_for_species():
    component = make_hydrogen_component(2.5)
    state = ChemicalState(components=(component,))

    resolved = StateResolver.resolve(state)

    assert resolved.moles_of(component.species) == pytest.approx(2.5)


def test_resolver_returns_zero_for_absent_species():
    component = make_hydrogen_component()
    other = make_oxygen_component()
    state = ChemicalState(components=(component,))

    resolved = StateResolver.resolve(state)

    assert resolved.moles_of(other.species) == 0.0


def test_resolver_rejects_invalid_state():
    with pytest.raises(TypeError):
        StateResolver.resolve("not a state")
