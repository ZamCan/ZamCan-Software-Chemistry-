import pytest

from knowledge.elements.loaders import (
    RawElementProperty,
    RawElementRecord,
)


def test_element_property_record():
    record = RawElementProperty(
        atomic_number=1,
        property_name="standard_atomic_weight",
        value=1.008,
        unit="g/mol",
        source="IUPAC/CIAAW",
    )

    assert record.atomic_number == 1
    assert record.property_name == "standard_atomic_weight"
    assert record.value == 1.008
    assert record.unit == "g/mol"


def test_element_record_property_lookup():
    property_record = RawElementProperty(
        atomic_number=8,
        property_name="standard_atomic_weight",
        value=15.999,
        unit="g/mol",
    )

    record = RawElementRecord(
        atomic_number=8,
        name="Oxygen",
        symbol="O",
        properties=(property_record,),
    )

    assert (
        record.property("standard_atomic_weight")
        == property_record
    )


def test_property_element_mismatch_rejected():
    property_record = RawElementProperty(
        atomic_number=8,
        property_name="density",
        value=1.0,
        unit="g/cm3",
    )

    with pytest.raises(ValueError):
        RawElementRecord(
            atomic_number=1,
            name="Hydrogen",
            symbol="H",
            properties=(property_record,),
        )


def test_negative_uncertainty_rejected():
    with pytest.raises(ValueError):
        RawElementProperty(
            atomic_number=1,
            property_name="density",
            value=1.0,
            uncertainty=-1.0,
        )
