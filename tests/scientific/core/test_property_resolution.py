from __future__ import annotations

import pytest

from scm.core import (
    Conditions,
    PropertyKind,
    PropertyRequest,
    Quantity,
    ResolutionStatus,
    ScientificPropertyResolver,
    ScientificStatus,
)

from knowledge.elements.properties import ElementPropertyData


resolver = ScientificPropertyResolver()


def make_record(
    *,
    temperature: float | None = None,
    status: ScientificStatus = ScientificStatus.KNOWN,
    notes: str = "resolver test",
) -> ElementPropertyData:
    conditions = None

    if temperature is not None:
        conditions = Conditions(
            temperature=Quantity(temperature, "K"),
        )

    return ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(3823.0, "K"),
        status=status,
        conditions=conditions,
        notes=notes,
    )


def make_request(
    *,
    temperature: float | None = None,
) -> PropertyRequest:
    conditions = None

    if temperature is not None:
        conditions = Conditions(
            temperature=Quantity(temperature, "K"),
        )

    return PropertyRequest(
        kind=PropertyKind.MELTING_POINT,
        conditions=conditions,
    )


def test_no_candidates_are_unavailable():
    result = resolver.resolve(
        make_request(),
        (),
    )

    assert result.status is ResolutionStatus.UNAVAILABLE
    assert result.value is None
    assert result.candidates == ()
    assert not result.resolved
    assert not result.usable


def test_one_matching_candidate_is_resolved():
    record = make_record()

    result = resolver.resolve(
        make_request(),
        (record,),
    )

    assert result.status is ResolutionStatus.RESOLVED
    assert result.value is record
    assert result.candidates == (record,)
    assert result.resolved
    assert result.usable


def test_multiple_matching_candidates_are_ambiguous():
    record_a = make_record(
        status=ScientificStatus.KNOWN,
        notes="candidate A",
    )
    record_b = make_record(
        status=ScientificStatus.OBSERVED,
        notes="candidate B",
    )

    result = resolver.resolve(
        make_request(),
        (record_a, record_b),
    )

    assert result.status is ResolutionStatus.AMBIGUOUS
    assert result.value is None
    assert result.candidates == (record_a, record_b)
    assert not result.resolved
    assert not result.usable


def test_property_kind_filters_candidates():
    record = ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.BOILING_POINT,
        quantity=Quantity(5100.0, "K"),
        status=ScientificStatus.KNOWN,
    )

    result = resolver.resolve(
        make_request(),
        (record,),
    )

    assert result.status is ResolutionStatus.UNAVAILABLE
    assert result.value is None
    assert result.candidates == ()


def test_matching_conditions_select_one_candidate():
    record_a = make_record(
        temperature=298.15,
        notes="298 K record",
    )
    record_b = make_record(
        temperature=350.0,
        notes="350 K record",
    )

    result = resolver.resolve(
        make_request(temperature=298.15),
        (record_a, record_b),
    )

    assert result.status is ResolutionStatus.RESOLVED
    assert result.value is record_a
    assert result.candidates == (record_a,)


def test_nonmatching_conditions_are_excluded():
    record = make_record(
        temperature=350.0,
    )

    result = resolver.resolve(
        make_request(temperature=298.15),
        (record,),
    )

    assert result.status is ResolutionStatus.UNAVAILABLE
    assert result.value is None
    assert result.candidates == ()


def test_unspecified_stored_conditions_remain_compatible():
    record = make_record()

    result = resolver.resolve(
        make_request(temperature=298.15),
        (record,),
    )

    assert result.status is ResolutionStatus.RESOLVED
    assert result.value is record


def test_invalid_request_is_rejected():
    with pytest.raises(TypeError):
        resolver.resolve(
            "not a request",
            (),
        )


def test_invalid_candidates_container_is_rejected():
    with pytest.raises(TypeError):
        resolver.resolve(
            make_request(),
            "not a candidate collection",
        )


def test_invalid_candidate_record_is_rejected():
    with pytest.raises(TypeError):
        resolver.resolve(
            make_request(),
            (object(),),
        )


def test_incompatible_temperature_dimension_does_not_match():
    record = make_record(
        temperature=298.15,
    )

    request = PropertyRequest(
        kind=PropertyKind.MELTING_POINT,
        conditions=Conditions(
            temperature=Quantity(1.0, "mol"),
        ),
    )

    result = resolver.resolve(
        request,
        (record,),
    )

    assert result.status is ResolutionStatus.UNAVAILABLE
    assert result.value is None
    assert result.candidates == ()


def test_temperature_condition_resolution_converts_offset_units():
    from scm.core import Conditions, Quantity

    stored = ElementPropertyData(
        atomic_number=1,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(1.0, "K"),
        status=ScientificStatus.KNOWN,
        conditions=Conditions(
            temperature=Quantity(298.15, "K"),
        ),
    )

    request = PropertyRequest(
        kind=PropertyKind.MELTING_POINT,
        conditions=Conditions(
            temperature=Quantity(25.0, "degC"),
        ),
    )

    result = ScientificPropertyResolver().resolve(
        request,
        (stored,),
    )

    assert result.status is ResolutionStatus.RESOLVED
    assert result.value is stored
