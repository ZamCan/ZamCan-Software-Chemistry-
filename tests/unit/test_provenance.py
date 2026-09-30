import pytest

from scm.core import Evidence, EvidenceType
from scm.core.provenance import EvidenceSummary, summarize_evidence


def test_empty_evidence_summary():
    summary = summarize_evidence(None)

    assert isinstance(summary, EvidenceSummary)
    assert summary.count == 0
    assert summary.types == frozenset()
    assert not summary.has_experimental
    assert not summary.has_reference
    assert not summary.has_computational
    assert not summary.has_theoretical
    assert not summary.has_observational


def test_single_evidence_summary():
    evidence = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC",
    )

    summary = summarize_evidence(evidence)

    assert summary.count == 1
    assert summary.types == frozenset({EvidenceType.REFERENCE})
    assert summary.has_reference
    assert not summary.has_experimental


def test_multiple_evidence_types_are_detected():
    evidence = (
        Evidence(evidence_type=EvidenceType.REFERENCE),
        Evidence(evidence_type=EvidenceType.EXPERIMENTAL),
        Evidence(evidence_type=EvidenceType.COMPUTATIONAL),
    )

    summary = summarize_evidence(evidence)

    assert summary.count == 3
    assert summary.types == frozenset({
        EvidenceType.REFERENCE,
        EvidenceType.EXPERIMENTAL,
        EvidenceType.COMPUTATIONAL,
    })
    assert summary.has_reference
    assert summary.has_experimental
    assert summary.has_computational
    assert not summary.has_theoretical
    assert not summary.has_observational


def test_has_type_requires_evidence_type():
    summary = summarize_evidence(None)

    with pytest.raises(TypeError):
        summary.has_type("reference")


def test_summary_preserves_evidence_records():
    first = Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="Source A",
    )
    second = Evidence(
        evidence_type=EvidenceType.OBSERVATIONAL,
        source="Source B",
    )

    summary = summarize_evidence((first, second))

    assert summary.evidence == (first, second)
    assert summary.evidence[0] is first
    assert summary.evidence[1] is second
