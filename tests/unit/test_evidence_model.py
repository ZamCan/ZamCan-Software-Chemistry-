import pytest

from scm.core import Evidence, EvidenceType


def test_evidence_creation():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC / CIAAW",
        reference="IUPAC Periodic Table",
        notes="Reference data",
    )

    assert evidence.evidence_type is EvidenceType.REFERENCE
    assert evidence.source == "IUPAC / CIAAW"
    assert evidence.reference == "IUPAC Periodic Table"
    assert evidence.notes == "Reference data"


def test_evidence_type_must_be_evidence_type():
    with pytest.raises(TypeError):
        Evidence(
            evidence_type="reference",
        )


def test_source_must_be_string_or_none():
    with pytest.raises(TypeError):
        Evidence(
            evidence_type=EvidenceType.REFERENCE,
            source=123,
        )


def test_reference_must_be_string_or_none():
    with pytest.raises(TypeError):
        Evidence(
            evidence_type=EvidenceType.REFERENCE,
            reference=123,
        )


def test_notes_must_be_string_or_none():
    with pytest.raises(TypeError):
        Evidence(
            evidence_type=EvidenceType.REFERENCE,
            notes=123,
        )


def test_optional_metadata_can_be_omitted():
    evidence = Evidence(
        evidence_type=EvidenceType.EXPERIMENTAL,
    )

    assert evidence.source is None
    assert evidence.reference is None
    assert evidence.notes is None


def test_evidence_string_prefers_source_and_reference():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
        reference="Periodic Table",
    )

    assert str(evidence) == "IUPAC: Periodic Table"


def test_evidence_string_uses_source_when_reference_missing():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
    )

    assert str(evidence) == "IUPAC"


def test_evidence_string_uses_reference_when_source_missing():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        reference="Periodic Table",
    )

    assert str(evidence) == "Periodic Table"


def test_evidence_string_falls_back_to_type():
    evidence = Evidence(
        evidence_type=EvidenceType.COMPUTATIONAL,
    )

    assert str(evidence) == "computational"
