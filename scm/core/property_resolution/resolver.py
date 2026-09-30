from __future__ import annotations

from typing import Any

from .request import PropertyRequest
from .result import (
    PropertyResolution,
    ResolutionStatus,
)


class ScientificPropertyResolver:
    """
    Conservative resolver for scientific property records.

    The resolver deliberately does not select a record merely
    because it appears first in a registry.

    Resolution policy for this foundation layer:

        no compatible records
            -> UNAVAILABLE

        exactly one compatible record
            -> RESOLVED

        multiple compatible records
            -> AMBIGUOUS

    More advanced scientific reconciliation policies can be
    added later without changing the basic request/result model.
    """

    def resolve(
        self,
        request: PropertyRequest,
        candidates: tuple[Any, ...] | list[Any],
    ) -> PropertyResolution[Any]:
        if not isinstance(request, PropertyRequest):
            raise TypeError(
                "request must be a PropertyRequest"
            )

        if not isinstance(candidates, (tuple, list)):
            raise TypeError(
                "candidates must be a tuple or list"
            )

        candidate_records = tuple(candidates)

        for candidate in candidate_records:
            self._validate_candidate(candidate)

        matching = tuple(
            candidate
            for candidate in candidate_records
            if candidate.kind is request.kind
            and candidate.matches_conditions(
                request.conditions
            )
        )

        if not matching:
            return PropertyResolution(
                status=ResolutionStatus.UNAVAILABLE,
                reasons=(
                    "no scientific property record matches "
                    "the requested property and conditions",
                ),
            )

        if len(matching) > 1:
            return PropertyResolution(
                status=ResolutionStatus.AMBIGUOUS,
                candidates=matching,
                reasons=(
                    "multiple scientific property records match "
                    "the requested property and conditions",
                ),
            )

        return PropertyResolution(
            status=ResolutionStatus.RESOLVED,
            value=matching[0],
            candidates=matching,
        )

    @staticmethod
    def _validate_candidate(candidate: Any) -> None:
        required_attributes = (
            "kind",
            "matches_conditions",
        )

        missing = tuple(
            attribute
            for attribute in required_attributes
            if not hasattr(candidate, attribute)
        )

        if missing:
            raise TypeError(
                "candidate is not a compatible scientific "
                "property record; missing: "
                + ", ".join(missing)
            )


__all__ = [
    "ScientificPropertyResolver",
]
