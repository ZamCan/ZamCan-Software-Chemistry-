from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChemistryContext:
    """
    Shared execution context for collaborating chemistry modules.

    Modules may operate independently without a context, but when
    combined, the context provides a common place for conditions,
    assumptions, metadata, and intermediate scientific information.
    """

    conditions: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_condition(self, condition: str) -> "ChemistryContext":
        if not condition.strip():
            raise ValueError("condition must not be empty")

        return ChemistryContext(
            conditions=self.conditions + (condition,),
            assumptions=self.assumptions,
            metadata=dict(self.metadata),
        )

    def with_assumption(self, assumption: str) -> "ChemistryContext":
        if not assumption.strip():
            raise ValueError("assumption must not be empty")

        return ChemistryContext(
            conditions=self.conditions,
            assumptions=self.assumptions + (assumption,),
            metadata=dict(self.metadata),
        )
