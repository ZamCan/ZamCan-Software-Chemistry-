from __future__ import annotations

from .module import ChemistryModule


class ChemistryModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ChemistryModule] = {}

    def register(self, module: ChemistryModule) -> None:
        if not isinstance(module, ChemistryModule):
            raise TypeError("module must implement ChemistryModule")

        if module.name in self._modules:
            raise ValueError(f"module already registered: {module.name}")

        self._modules[module.name] = module

    def get(self, name: str) -> ChemistryModule:
        try:
            return self._modules[name]
        except KeyError as exc:
            raise KeyError(f"unknown chemistry module: {name}") from exc

    def all(self) -> tuple[ChemistryModule, ...]:
        return tuple(self._modules.values())

    def find_capability(self, capability: str) -> tuple[ChemistryModule, ...]:
        return tuple(
            module
            for module in self._modules.values()
            if module.can_handle(capability)
        )
