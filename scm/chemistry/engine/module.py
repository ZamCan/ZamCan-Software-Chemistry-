from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ChemistryModule(ABC):
    """
    Base contract for independently usable and composable chemistry modules.
    """

    name: str = "unnamed"

    @abstractmethod
    def capabilities(self) -> frozenset[str]:
        """Return stable capability identifiers."""

    def can_handle(self, capability: str) -> bool:
        return capability in self.capabilities()

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "capabilities": sorted(self.capabilities()),
        }
