import pytest

from scm.core import Quantity
from scm.chemistry.amount import AmountOfSubstance
from scm.chemistry.reactions import (
    MaterialRole,
    ReactionMaterialBalance,
    ReactionMaterialBalanceCalculator,
    ReactionStoichiometry,
    StoichiometricTerm,
    reaction_material_balance_calculator,
)
from scm.matter.species import ChemicalSpecies
from scm.matter.states import ChemicalState, StateComponent


def species(formula: str) -> ChemicalSpecies:
    mapping = {}

    import re

    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)

    for symbol, count in tokens:
        mapping[symbol] = mapping.get(symbol, 0) + (
            int(count) if count else 1
        )

    from scm.matter.composition import Composition

    return ChemicalSpecies(
        composition=Composition.from_mapping(mapping)
    )


def component(
    formula: str,
    moles: float,
) -> StateComponent:
    return StateComponent(
        species=species(formula),
        amount=AmountOfSubstance(
            Quantity(moles, "mol"),
            entity="molecules",
        ),
    )


def state(*components: StateComponent) -> ChemicalState:
    return ChemicalState.from_components(
        tuple(components),
    )


def reaction(
    reactants: tuple[tuple[str, int], ...],
    products: tuple[tuple[str, int], ...],
) -> ReactionStoichiometry:
    return ReactionStoichiometry.from_terms(
        reactants=tuple(
            StoichiometricTerm(
                species=species(formula),
                coefficient=coefficient,
            )
            for formula, coefficient in reactants
        ),
        products=tuple(
            StoichiometricTerm(
                species=species(formula),
                coefficient=coefficient,
            )
            for formula, coefficient in products
        ),
    )


def test_limiting_reactant_and_excess_remainder():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 3.0),
        component("O2", 1.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
    )

    assert result.extent.to("mol").value == pytest.approx(1.0)
    assert result.limiting_species == species("O2")

    h2 = result.balance_for(species("H2"))
    o2 = result.balance_for(species("O2"))
    h2o = result.balance_for(species("H2O"))

    assert h2.role is MaterialRole.REACTANT
    assert h2.initial_moles == pytest.approx(3.0)
    assert h2.change_moles == pytest.approx(-2.0)
    assert h2.final_moles == pytest.approx(1.0)

    assert o2.initial_moles == pytest.approx(1.0)
    assert o2.change_moles == pytest.approx(-1.0)
    assert o2.final_moles == pytest.approx(0.0)

    assert h2o.role is MaterialRole.PRODUCT
    assert h2o.initial_moles == pytest.approx(0.0)
    assert h2o.change_moles == pytest.approx(2.0)
    assert h2o.final_moles == pytest.approx(2.0)


def test_partial_extent_leaves_reactants_and_generates_partial_product():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 5.0),
        component("O2", 3.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
        extent=Quantity(1.5, "mol"),
    )

    assert result.extent.to("mol").value == pytest.approx(1.5)

    assert result.balance_for(species("H2")).final_moles == pytest.approx(2.0)
    assert result.balance_for(species("O2")).final_moles == pytest.approx(1.5)
    assert result.balance_for(species("H2O")).final_moles == pytest.approx(3.0)


def test_initially_absent_product_is_created_in_material_accounting():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 2.0),
        component("O2", 1.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
    )

    water = result.balance_for(species("H2O"))

    assert water.initial_moles == pytest.approx(0.0)
    assert water.change_moles == pytest.approx(2.0)
    assert water.final_moles == pytest.approx(2.0)
    assert water.generated


def test_supplied_extent_cannot_exceed_available_reactants():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 2.0),
        component("O2", 1.0),
    )

    with pytest.raises(
        ValueError,
        match="exceeds the stoichiometrically available extent",
    ):
        reaction_material_balance_calculator.calculate(
            rxn,
            initial,
            extent=Quantity(1.1, "mol"),
        )


def test_zero_extent_leaves_all_material_unchanged():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 3.0),
        component("O2", 2.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
        extent=Quantity(0.0, "mol"),
    )

    for formula, amount in (
        ("H2", 3.0),
        ("O2", 2.0),
    ):
        balance = result.balance_for(species(formula))

        assert balance.initial_moles == pytest.approx(amount)
        assert balance.change_moles == pytest.approx(0.0)
        assert balance.final_moles == pytest.approx(amount)
        assert balance.unchanged

    water = result.balance_for(species("H2O"))

    assert water.initial_moles == pytest.approx(0.0)
    assert water.change_moles == pytest.approx(0.0)
    assert water.final_moles == pytest.approx(0.0)


def test_duplicate_state_components_are_aggregated():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 1.0),
        component("H2", 2.0),
        component("O2", 1.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
    )

    h2 = result.balance_for(species("H2"))

    assert h2.initial_moles == pytest.approx(3.0)
    assert h2.change_moles == pytest.approx(-2.0)
    assert h2.final_moles == pytest.approx(1.0)


def test_consumed_and_generated_species_are_classified():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 2.0),
        component("O2", 1.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
    )

    assert {b.species for b in result.consumed_species} == {
        species("H2"),
        species("O2"),
    }

    assert {b.species for b in result.generated_species} == {
        species("H2O"),
    }


def test_remaining_species_contains_only_positive_final_amounts():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 3.0),
        component("O2", 1.0),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
    )

    remaining = {
        balance.species
        for balance in result.remaining_species
    }

    assert species("H2") in remaining
    assert species("H2O") in remaining
    assert species("O2") not in remaining


def test_species_material_balance_rejects_inconsistent_final_amount():
    with pytest.raises(
        ValueError,
        match="final_amount must equal",
    ):
        from scm.chemistry.reactions.material_balance import (
            SpeciesMaterialBalance,
        )

        SpeciesMaterialBalance(
            species=species("H2"),
            role=MaterialRole.REACTANT,
            initial_amount=Quantity(2.0, "mol"),
            change=Quantity(-1.0, "mol"),
            final_amount=Quantity(2.0, "mol"),
        )


def test_species_material_balance_rejects_negative_initial_amount():
    from scm.chemistry.reactions.material_balance import (
        SpeciesMaterialBalance,
    )

    with pytest.raises(
        ValueError,
        match="initial_amount cannot be negative",
    ):
        SpeciesMaterialBalance(
            species=species("H2"),
            role=MaterialRole.REACTANT,
            initial_amount=Quantity(-1.0, "mol"),
            change=Quantity(0.0, "mol"),
            final_amount=Quantity(-1.0, "mol"),
        )


def test_species_material_balance_rejects_negative_final_amount():
    from scm.chemistry.reactions.material_balance import (
        SpeciesMaterialBalance,
    )

    with pytest.raises(
        ValueError,
        match="final_amount cannot be negative",
    ):
        SpeciesMaterialBalance(
            species=species("H2"),
            role=MaterialRole.REACTANT,
            initial_amount=Quantity(1.0, "mol"),
            change=Quantity(-2.0, "mol"),
            final_amount=Quantity(-1.0, "mol"),
        )


def test_material_balance_preserves_mole_accounting():
    rxn = reaction(
        (("H2", 2), ("O2", 1)),
        (("H2O", 2),),
    )

    initial = state(
        component("H2", 5.0),
        component("O2", 3.0),
        component("H2O", 0.5),
    )

    result = reaction_material_balance_calculator.calculate(
        rxn,
        initial,
        extent=Quantity(2.0, "mol"),
    )

    h2 = result.balance_for(species("H2"))
    o2 = result.balance_for(species("O2"))
    h2o = result.balance_for(species("H2O"))

    assert h2.initial_moles + h2.change_moles == pytest.approx(
        h2.final_moles
    )
    assert o2.initial_moles + o2.change_moles == pytest.approx(
        o2.final_moles
    )
    assert h2o.initial_moles + h2o.change_moles == pytest.approx(
        h2o.final_moles
    )


def test_public_calculator_is_available():
    assert isinstance(
        reaction_material_balance_calculator,
        ReactionMaterialBalanceCalculator,
    )
