from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class RuleStatus(str, Enum):
    """
    High-level outcome of evaluating a scientific rule.
    """

    PASSED = "passed"
    FAILED = "failed"
    INCONCLUSIVE = "inconclusive"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class RuleResult:
    """
    Immutable result produced by a Rule evaluation.

    A result describes what the rule concluded without
    pretending that every conclusion is an absolute fact.
    """

    status: RuleStatus
    reason: str
    details: Mapping[str, Any] | None = None

    @property
    def passed(self) -> bool:
        return self.status is RuleStatus.PASSED

    @property
    def failed(self) -> bool:
        return self.status is RuleStatus.FAILED

    @property
    def conclusive(self) -> bool:
        return self.status in {
            RuleStatus.PASSED,
            RuleStatus.FAILED,
        }


class Rule:
    """
    Base contract for reusable scientific reasoning rules.

    Rules should describe scientific constraints or relationships.
    They should not contain UI, HTTP, persistence, or presentation logic.
    """

    name: str = "unnamed_rule"
    domain: str = "general"

    def describe(self) -> str:
        return self.name

    def can_apply(self, *inputs: Any, **context: Any) -> bool:
        """
        Return whether this rule can meaningfully evaluate the supplied input.
        """
        return True

    def evaluate(self, *inputs: Any, **context: Any) -> RuleResult:
        """
        Evaluate the rule.

        Concrete rules must implement this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.evaluate() must be implemented"
        )
