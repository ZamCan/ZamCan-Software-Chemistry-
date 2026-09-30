from __future__ import annotations

from dataclasses import dataclass

from .enums import EvidenceType
from .evidence import Evidence, normalize_evidence


@dataclass(frozen=True)
class EvidenceSummary:
    """
    Read-only summary of the evidence supporting a scientific claim.

    This class describes the available evidence without judging
    scientific truth or changing the claim's ScientificStatus.
    """

    evidence: tuple[Evidence, ...]

    def __post_init__(self) -> None:
        normalized = normalize_evidence(self.evidence)

        object.__setattr__(
            self,
            "evidence",
            normalized,
        )

    @property
    def count(self) -> int:
        return len(self.evidence)

    @property
    def types(self) -> frozenset[EvidenceType]:
        return frozenset(
            evidence.evidence_type
            for evidence in self.evidence
        )

    def has_type(self, evidence_type: EvidenceType) -> bool:
        if not isinstance(evidence_type, EvidenceType):
            raise TypeError(
                "evidence_type must be an EvidenceType"
            )

        return evidence_type in self.types

    @property
    def has_experimental(self) -> bool:
        return self.has_type(EvidenceType.EXPERIMENTAL)

    @property
    def has_reference(self) -> bool:
        return self.has_type(EvidenceType.REFERENCE)

    @property
    def has_computational(self) -> bool:
        return self.has_type(EvidenceType.COMPUTATIONAL)

    @property
    def has_theoretical(self) -> bool:
        return self.has_type(EvidenceType.THEORETICAL)

    @property
    def has_observational(self) -> bool:
        return self.has_type(EvidenceType.OBSERVATIONAL)


def summarize_evidence(
    evidence: Evidence | tuple[Evidence, ...] | None,
) -> EvidenceSummary:
    """
    Create a read-only summary from zero or more evidence records.
    """

    return EvidenceSummary(
        evidence=normalize_evidence(evidence),
    )


__all__ = [
    "EvidenceSummary",
    "summarize_evidence",
]
