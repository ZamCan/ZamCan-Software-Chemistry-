from knowledge.elements.properties import (
    ElementPropertyData,
    PropertyIdentity,
    get_atomic_properties_by_identity,
    get_atomic_properties_by_identity_and_conditions,
    get_atomic_properties_by_kind,
    get_atomic_properties_matching_conditions,
    get_atomic_property,
    register_atomic_property,
)

from scm.core import (
    Conditions,
    PropertyKind,
    Quantity,
    ScientificStatus,
)


def make_record(
    *,
    temperature,
    status,
    notes,
):
    return ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(3823.0, "K"),
        status=status,
        conditions=Conditions(
            temperature=Quantity(temperature, "K"),
        ),
        notes=notes,
    )


def test_multiple_records_can_share_one_identity():
    record_a = make_record(
        temperature=298.15,
        status=ScientificStatus.KNOWN,
        notes="registry test A",
    )

    record_b = make_record(
        temperature=300.0,
        status=ScientificStatus.OBSERVED,
        notes="registry test B",
    )

    register_atomic_property(record_a)
    register_atomic_property(record_b)

    identity = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    records = get_atomic_properties_by_identity(identity)

    assert record_a in records
    assert record_b in records


def test_query_by_kind_returns_all_matching_records():
    record_a = make_record(
        temperature=310.0,
        status=ScientificStatus.KNOWN,
        notes="kind test A",
    )

    record_b = make_record(
        temperature=320.0,
        status=ScientificStatus.OBSERVED,
        notes="kind test B",
    )

    register_atomic_property(record_a)
    register_atomic_property(record_b)

    records = get_atomic_properties_by_kind(
        6,
        PropertyKind.MELTING_POINT,
    )

    assert record_a in records
    assert record_b in records


def test_identity_and_condition_query_filters_records():
    record_a = make_record(
        temperature=330.0,
        status=ScientificStatus.KNOWN,
        notes="condition test A",
    )

    record_b = make_record(
        temperature=340.0,
        status=ScientificStatus.OBSERVED,
        notes="condition test B",
    )

    register_atomic_property(record_a)
    register_atomic_property(record_b)

    identity = PropertyIdentity(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
    )

    requested = Conditions(
        temperature=Quantity(330.0, "K"),
    )

    records = get_atomic_properties_by_identity_and_conditions(
        identity,
        requested,
    )

    assert record_a in records
    assert record_b not in records


def test_condition_query_by_atomic_number_and_kind():
    record_a = make_record(
        temperature=350.0,
        status=ScientificStatus.KNOWN,
        notes="matching test",
    )

    record_b = make_record(
        temperature=360.0,
        status=ScientificStatus.OBSERVED,
        notes="nonmatching test",
    )

    register_atomic_property(record_a)
    register_atomic_property(record_b)

    requested = Conditions(
        temperature=Quantity(350.0, "K"),
    )

    records = get_atomic_properties_matching_conditions(
        6,
        PropertyKind.MELTING_POINT,
        requested,
    )

    assert record_a in records
    assert record_b not in records


def test_legacy_singular_query_remains_functional():
    record = make_record(
        temperature=370.0,
        status=ScientificStatus.KNOWN,
        notes="legacy API test",
    )

    register_atomic_property(record)

    result = get_atomic_property(
        6,
        PropertyKind.MELTING_POINT,
    )

    assert result is not None
    assert result.kind is PropertyKind.MELTING_POINT
