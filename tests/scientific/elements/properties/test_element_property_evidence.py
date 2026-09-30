from knowledge.elements.properties import (
    ElementPropertyData,
)
from scm.core import (
    Evidence,
    EvidenceType,
    PropertyKind,
    Quantity,
    ScientificStatus,
)


def make_evidence(
    *,
    source: str,
    evidence_type: EvidenceType = EvidenceType.REFERENCE,
) -> Evidence:
    return Evidence(
        evidence_type=evidence_type,
        source=source,
    )


def make_property_data(
    *,
    evidence,
) -> ElementPropertyData:
    return ElementPropertyData(
        atomic_number=6,
        kind=PropertyKind.MELTING_POINT,
        quantity=Quantity(3823.0, "K"),
        status=ScientificStatus.KNOWN,
        evidence=evidence,
    )


def test_single_evidence_is_normalized():
    evidence = make_evidence(
        source="IUPAC",
    )

    record = make_property_data(
        evidence=evidence,
    )

    assert record.evidence == (evidence,)
    assert record.primary_evidence is evidence


def test_multiple_evidence_records_are_preserved():
    evidence_a = make_evidence(
        source="IUPAC",
    )

    evidence_b = make_evidence(
        source="Experimental study",
        evidence_type=EvidenceType.EXPERIMENTAL,
    )

    record = make_property_data(
        evidence=(evidence_a, evidence_b),
    )

    assert record.evidence == (
        evidence_a,
        evidence_b,
    )


def test_no_evidence_becomes_empty_tuple():
    record = make_property_data(
        evidence=None,
    )

    assert record.evidence == ()
    assert record.primary_evidence is None


def test_evidence_is_preserved_during_conversion():
    evidence_a = make_evidence(
        source="Reference source",
    )

    evidence_b = make_evidence(
        source="Independent experiment",
        evidence_type=EvidenceType.EXPERIMENTAL,
    )

    record = make_property_data(
        evidence=(evidence_a, evidence_b),
    )

    prop = record.to_scientific_property(
        "melting point",
    )

    assert prop.evidence == (
        evidence_a,
        evidence_b,
    )

    assert prop.primary_evidence is evidence_a
