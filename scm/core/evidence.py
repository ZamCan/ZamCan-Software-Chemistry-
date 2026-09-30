from __future__ import annotations

from dataclasses import dataclass


from .enums import EvidenceType


@dataclass(frozen=True)
class Evidence:
    """
    Scientific provenance supporting a knowledge record.

    Evidence describes where a scientific claim comes from.
    It is intentionally independent from the claim's scientific
    status because one claim may have multiple supporting sources.
    """

    evidence_type: EvidenceType
    source: str | None = None
    reference: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.evidence_type,
            EvidenceType,
        ):
            raise TypeError(
                "evidence_type must be an EvidenceType"
            )

        for field_name, value in (
            ("source", self.source),
            ("reference", self.reference),
            ("notes", self.notes),
        ):
            if value is not None and not isinstance(
                value,
                str,
            ):
                raise TypeError(
                    f"{field_name} must be a string or None"
                )

    def __str__(self) -> str:
        if self.source and self.reference:
            return f"{self.source}: {self.reference}"

        if self.source:
            return self.source

        if self.reference:
            return self.reference

        return self.evidence_type.value


def normalize_evidence(
    evidence: Evidence | tuple[Evidence, ...] | None,
) -> tuple[Evidence, ...]:
    """
    Normalize one or more evidence records into an immutable tuple.

    Supported inputs:
        None
        Evidence
        tuple[Evidence, ...]

    This provides a controlled migration path from the original
    single-evidence API to the multi-evidence architecture.
    """

    if evidence is None:
        return ()

    if isinstance(evidence, Evidence):
        return (evidence,)

    if not isinstance(evidence, tuple):
        raise TypeError(
            "evidence must be Evidence, tuple[Evidence, ...], or None"
        )

    for item in evidence:
        if not isinstance(item, Evidence):
            raise TypeError(
                "every evidence item must be an Evidence instance"
            )

    return evidence


__all__ = [
    "Evidence",
    "normalize_evidence",
]
