import pytest

from knowledge.elements.loaders import (
    ElementPropertyAdapter,
    RawElementProperty,
    RawElementRecord,
)
from scm.core import PropertyKind, ScientificStatus


def test_adapter_converts_standard_atomic_weight():
    raw = RawElementRecord(
        atomic_number=1,
        name="Hydrogen",
        symbol="H",
        properties=(
            RawElementProperty(
                atomic_number=1,
                property_name="standard_atomic_weight",
                value=1.008,
                unit="g/mol",
                source="IUPAC/CIAAW",
                reference="Standard Atomic Weights",
            ),
        ),
    )

    converted = ElementPropertyAdapter.convert(raw)

    assert len(converted) == 1
    assert converted[0].atomic_number == 1
    assert (
        converted[0].kind
        is PropertyKind.STANDARD_ATOMIC_WEIGHT
    )
    assert converted[0].status is ScientificStatus.KNOWN
    assert converted[0].quantity.value == 1.008


def test_adapter_preserves_uncertainty():
    raw = RawElementRecord(
        atomic_number=8,
        name="Oxygen",
        symbol="O",
        properties=(
            RawElementProperty(
                atomic_number=8,
                property_name="density",
                value=1.0,
                unit="g/cm3",
                uncertainty=0.01,
            ),
        ),
    )

    converted = ElementPropertyAdapter.convert(raw)

    assert converted[0].uncertainty is not None
    assert converted[0].uncertainty.absolute == 0.01


def test_missing_value_is_not_guessed():
    raw = RawElementRecord(
        atomic_number=1,
        name="Hydrogen",
        symbol="H",
        properties=(
            RawElementProperty(
                atomic_number=1,
                property_name="density",
                value=None,
                unit=None,
            ),
        ),
    )

    with pytest.raises(ValueError):
        ElementPropertyAdapter.convert(raw)
