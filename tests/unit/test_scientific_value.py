import pytest

from scm.core.scientific_values import (
    ScientificValue,
    ValueRelation,
)


def test_exact_value():
    value = ScientificValue(
        value=12.32,
        unit="y",
    )

    assert value.value == 12.32
    assert value.unit == "y"
    assert value.relation is ValueRelation.EXACT


def test_value_with_uncertainty():
    value = ScientificValue(
        value=12.32,
        unit="y",
        uncertainty=0.02,
    )

    assert value.uncertainty == 0.02


def test_approximate_value():
    value = ScientificValue(
        value=12.32,
        unit="y",
        relation=ValueRelation.APPROXIMATE,
    )

    assert value.relation is ValueRelation.APPROXIMATE


def test_lower_limit():
    value = ScientificValue(
        value=1.0e20,
        unit="y",
        relation=ValueRelation.LOWER_LIMIT,
    )

    assert value.relation is ValueRelation.LOWER_LIMIT


def test_upper_limit():
    value = ScientificValue(
        value=1.0,
        unit="y",
        relation=ValueRelation.UPPER_LIMIT,
    )

    assert value.relation is ValueRelation.UPPER_LIMIT


def test_negative_uncertainty_rejected():
    with pytest.raises(ValueError):
        ScientificValue(
            value=1.0,
            unit="y",
            uncertainty=-0.1,
        )


def test_empty_unit_rejected():
    with pytest.raises(ValueError):
        ScientificValue(
            value=1.0,
            unit="",
        )
