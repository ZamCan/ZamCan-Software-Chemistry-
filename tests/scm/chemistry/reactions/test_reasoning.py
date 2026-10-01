from scm.chemistry.reactions import (
    ReactionOutcome,
    ReactionReasonCode,
    assess_reaction,
)


def test_noble_gas_reactivity_is_condition_dependent():
    result = assess_reaction(
        reactants=("Xe", "F2"),
    )

    assert result.outcome is ReactionOutcome.CONDITION_DEPENDENT
    assert result.primary_reason is not None
    assert result.primary_reason.code is ReactionReasonCode.NOBLE_GAS_STABILITY


def test_unknown_products_are_not_invented():
    result = assess_reaction(
        reactants=("Na", "Cl2"),
    )

    assert result.outcome is ReactionOutcome.UNDETERMINED
    assert result.primary_reason is not None
    assert result.primary_reason.code is ReactionReasonCode.INSUFFICIENT_DATA


def test_product_prediction_uses_registered_hydrogen_oxygen_rule():
    from scm.chemistry.reactions.prediction import product_prediction_engine
    from scm.chemistry.reactions.prediction.engine import PredictionStatus

    result = product_prediction_engine.predict(("H2", "O2"))

    assert result.products == ("H2O",)
    assert result.status is PredictionStatus.CONDITION_DEPENDENT
    assert result.evidence
