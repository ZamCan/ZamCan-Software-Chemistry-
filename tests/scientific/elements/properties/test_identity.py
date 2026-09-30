import pytest

from knowledge.elements.properties import (
    ElementPropertyData,
    PropertyIdentity,
)

from scm.core import (
    PropertyKind,
    Quantity,
    ScientificStatus,
)


def test_property_identity_creation():
    identity = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    assert identity.atomic_number == 6
    assert identity.kind is PropertyKind.MELTING_POINT


def test_property_identity_equality():
    first = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    second = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    assert first == second


def test_property_identity_is_hashable():
    first = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    second = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    identities = {first, second}

    assert len(identities) == 1


@pytest.mark.parametrize(
    "atomic_number",
    [0, -1, 119, 1000],
)
def test_invalid_atomic_number_is_rejected(
    atomic_number,
):
    with pytest.raises(ValueError):
        PropertyIdentity(
            atomic_number=atomic_number,
            kind=PropertyKind.MELTING_POINT,
        )


def test_invalid_property_kind_is_rejected():
    with pytest.raises(TypeError):
        PropertyIdentity(
            atomic_number=6,
            kind="melting_point",
        )


def test_element_property_data_identity_is_derived():
    property_data = ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(
            3823.0,
            "K",
        ),
        status=ScientificStatus.KNOWN,
    )

    expected = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    assert property_data.identity == expected


def test_element_property_data_identity_is_stable():
    property_data = ElementPropertyData(
        atomic_number=8,
        kind=PropertyKind.BOILING_POINT,
        quantity=Quantity(
            90.0,
            "K",
        ),
        status=ScientificStatus.KNOWN,
    )

    first = property_data.identity
    second = property_data.identity

    assert first == second
    assert hash(first) == hash(second)
