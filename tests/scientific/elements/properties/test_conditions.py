from knowledge.elements.properties import ElementPropertyData

from scm.core import (
    Conditions,
    PropertyKind,
    Quantity,
    ScientificStatus,
)


def make_record(
    *,
    temperature=None,
    pressure=None,
    atmosphere=None,
):
    return ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(3823.0, "K"),
        status=ScientificStatus.KNOWN,
        conditions=Conditions(
            temperature=temperature,
            pressure=pressure,
            atmosphere=atmosphere,
        ),
    )


def test_matching_conditions_are_accepted():
    record = make_record(
        temperature=Quantity(298.15, "K"),
        pressure=Quantity(101325.0, "Pa"),
        atmosphere="air",
    )

    requested = Conditions(
        temperature=Quantity(298.15, "K"),
        pressure=Quantity(101325.0, "Pa"),
        atmosphere="AIR",
    )

    assert record.matches_conditions(requested)


def test_conflicting_temperature_is_rejected():
    record = make_record(
        temperature=Quantity(298.15, "K"),
    )

    requested = Conditions(
        temperature=Quantity(300.0, "K"),
    )

    assert not record.matches_conditions(requested)


def test_conflicting_pressure_is_rejected():
    record = make_record(
        pressure=Quantity(101325.0, "Pa"),
    )

    requested = Conditions(
        pressure=Quantity(100000.0, "Pa"),
    )

    assert not record.matches_conditions(requested)


def test_partial_request_is_compatible():
    record = make_record(
        temperature=Quantity(298.15, "K"),
        pressure=Quantity(101325.0, "Pa"),
    )

    requested = Conditions(
        pressure=Quantity(101325.0, "Pa"),
    )

    assert record.matches_conditions(requested)


def test_missing_stored_conditions_are_unspecified():
    record = make_record()

    requested = Conditions(
        temperature=Quantity(298.15, "K"),
        pressure=Quantity(101325.0, "Pa"),
    )

    assert record.matches_conditions(requested)


def test_no_requested_conditions_matches():
    record = make_record(
        temperature=Quantity(298.15, "K"),
    )

    assert record.matches_conditions(None)


def test_solvent_matching_is_case_insensitive():
    record = make_record()

    record = ElementPropertyData(
        atomic_number=record.atomic_number,
        kind=record.kind,
        quantity=record.quantity,
        status=record.status,
        conditions=Conditions(
            solvent="water",
        ),
    )

    requested = Conditions(
        solvent="WATER",
    )

    assert record.matches_conditions(requested)


def test_atmosphere_matching_is_case_insensitive():
    record = make_record(
        atmosphere="air",
    )

    requested = Conditions(
        atmosphere="AIR",
    )

    assert record.matches_conditions(requested)
