import pytest

from scm.core import (
    Evidence,
    EvidenceType,
    PropertyKind,
    Quantity,
    ScientificProperty,
    ScientificStatus,
)


def test_scientific_property_accepts_multiple_evidence_records():
    reference = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
        reference="Reference table",
    )
    experiment = Evidence(
        evidence_type=EvidenceType.EXPERIMENTAL,
        source="Laboratory",
        reference="Experiment-001",
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(10.0, "1"),
        status=ScientificStatus.OBSERVED,
        kind=PropertyKind.OTHER,
        evidence=(reference, experiment),
    )

    assert prop.evidence == (reference, experiment)
    assert len(prop.evidence) == 2


def test_primary_evidence_returns_first_evidence_record():
    first = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="Source A",
    )
    second = Evidence(
        evidence_type=EvidenceType.EXPERIMENTAL,
        source="Source B",
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(10.0, "1"),
        status=ScientificStatus.KNOWN,
        evidence=(first, second),
    )

    assert prop.primary_evidence is first


def test_evidence_is_immutable_tuple():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
    )

    prop = ScientificProperty(
        name="test property",
        quantity=Quantity(10.0, "1"),
        status=ScientificStatus.KNOWN,
        evidence=evidence,
    )

    assert isinstance(prop.evidence, tuple)
    assert prop.evidence == (evidence,)


def test_invalid_multi_evidence_item_is_rejected():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
    )

    with pytest.raises(TypeError):
        ScientificProperty(
            name="test property",
            quantity=Quantity(10.0, "1"),
            status=ScientificStatus.KNOWN,
            evidence=(evidence, "not evidence"),
        )
