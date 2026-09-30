import pytest

from knowledge.isotopes import get_isotope
from knowledge.isotopes.properties import (
    IsotopePropertyData,
    IsotopePropertyIdentity,
    get_isotope_properties,
    get_isotope_properties_by_identity,
    get_isotope_properties_by_kind,
    get_isotope_property,
    register_isotope_property,
)
from knowledge.isotopes.properties import registry
from scm.core import (
    PropertyKind,
    Quantity,
    ScientificStatus,
)


@pytest.fixture(autouse=True)
def clear_isotope_property_registry():
    registry._ISOTOPE_PROPERTIES.clear()
    yield
    registry._ISOTOPE_PROPERTIES.clear()


def make_tritium_property(
    kind=PropertyKind.ATOMIC_MASS,
):
    return IsotopePropertyData(
        isotope=get_isotope("tritium"),
        kind=kind,
        quantity=Quantity(3.016049, "1"),
        status=ScientificStatus.KNOWN,
    )


def test_isotope_property_identity_uses_z_a_and_kind():
    identity = IsotopePropertyIdentity(
        atomic_number=1,
        mass_number=3,
        kind=PropertyKind.ATOMIC_MASS,
    )

    assert identity.atomic_number == 1
    assert identity.mass_number == 3
    assert identity.kind is PropertyKind.ATOMIC_MASS


def test_isotope_property_data_returns_correct_identity():
    record = make_tritium_property()

    assert record.identity == IsotopePropertyIdentity(
        atomic_number=1,
        mass_number=3,
        kind=PropertyKind.ATOMIC_MASS,
    )


def test_isotope_property_registry_lookup():
    record = make_tritium_property()

    register_isotope_property(record)

    assert get_isotope_properties((1, 3)) == (record,)


def test_isotope_property_registry_lookup_by_kind():
    record = make_tritium_property()

    register_isotope_property(record)

    assert get_isotope_properties_by_kind(
        (1, 3),
        PropertyKind.ATOMIC_MASS,
    ) == (record,)


def test_isotope_property_registry_lookup_by_identity():
    record = make_tritium_property()

    register_isotope_property(record)

    identity = IsotopePropertyIdentity(
        atomic_number=1,
        mass_number=3,
        kind=PropertyKind.ATOMIC_MASS,
    )

    assert get_isotope_properties_by_identity(identity) == (record,)


def test_first_isotope_property_can_be_retrieved():
    record = make_tritium_property()

    register_isotope_property(record)

    assert get_isotope_property(
        (1, 3),
        PropertyKind.ATOMIC_MASS,
    ) == record


def test_unknown_isotope_returns_no_properties():
    assert get_isotope_properties((1, 999)) == ()


def test_invalid_property_identity_is_rejected():
    with pytest.raises(ValueError):
        IsotopePropertyIdentity(
            atomic_number=1,
            mass_number=0,
            kind=PropertyKind.ATOMIC_MASS,
        )
