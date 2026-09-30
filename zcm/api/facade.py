from __future__ import annotations

from typing import Any

from scm.chemistry.engine import ChemistryModuleRegistry
from zcm.engine import zcm_registry


class ZCM:
    """
    Unified execution facade for ZCM modules.

    Modules remain independently usable while ZCM provides
    a common discovery and dispatch interface.
    """

    def __init__(
        self,
        registry: ChemistryModuleRegistry | None = None,
    ) -> None:
        self.registry = registry or zcm_registry

    def modules(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            module.describe()
            for module in self.registry.all()
        )

    def capabilities(self) -> frozenset[str]:
        capabilities: set[str] = set()

        for module in self.registry.all():
            capabilities.update(module.capabilities())

        return frozenset(capabilities)

    def find_modules(
        self,
        capability: str,
    ) -> tuple[Any, ...]:
        return self.registry.find_capability(capability)

    def execute(
        self,
        capability: str,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        modules = self.find_modules(capability)

        if not modules:
            raise LookupError(
                f"no module supports capability: {capability}"
            )

        if len(modules) > 1:
            raise LookupError(
                f"multiple modules support capability: {capability}"
            )

        target = getattr(modules[0], method, None)

        if target is None or not callable(target):
            raise AttributeError(
                f"module '{modules[0].name}' does not expose "
                f"method '{method}'"
            )

        return target(*args, **kwargs)


zcm = ZCM()


__all__ = [
    "ZCM",
    "zcm",
]
