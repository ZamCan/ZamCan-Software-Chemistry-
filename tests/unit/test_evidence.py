import pytest

from scm.core import (
    Evidence,
    EvidenceType,
    ScientificProperty,
    ScientificStatus,
    Quantity,
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


def test_single_evidence_is_normalized_to_tuple():
    evidence = make_evidence(
        source="IUPAC",
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(1.0, "K"),
        status=ScientificStatus.KNOWN,
        evidence=evidence,
    )

    assert prop.evidence == (evidence,)
    assert isinstance(prop.evidence, tuple)


def test_multiple_evidence_records_are_preserved():
    evidence_a = make_evidence(
        source="IUPAC",
    )

    evidence_b = make_evidence(
        source="Experimental study",
        evidence_type=EvidenceType.EXPERIMENTAL,
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(1.0, "K"),
        status=ScientificStatus.KNOWN,
        evidence=(evidence_a, evidence_b),
    )

    assert prop.evidence == (
        evidence_a,
        evidence_b,
    )


def test_primary_evidence_returns_first_record():
    evidence_a = make_evidence(
        source="Primary reference",
    )

    evidence_b = make_evidence(
        source="Secondary reference",
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(1.0, "K"),
        status=ScientificStatus.KNOWN,
        evidence=(evidence_a, evidence_b),
    )

    assert prop.primary_evidence is evidence_a


def test_no_evidence_becomes_empty_tuple():
    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(1.0, "K"),
        status=ScientificStatus.KNOWN,
    )

    assert prop.evidence == ()
    assert prop.primary_evidence is None


def test_invalid_evidence_item_is_rejected():
    with pytest.raises(TypeError):
        ScientificProperty(
            name="test property",
            quantity=Quantity(1.0, "K"),
            status=ScientificStatus.KNOWN,
            evidence=(make_evidence(source="valid"), "invalid"),
        )
