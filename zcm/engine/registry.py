from __future__ import annotations

from scm.chemistry.engine import ChemistryModuleRegistry

from zcm.catalog.elements import element_catalog
from zcm.chemistry.calculator import chemistry_calculator
from zcm.chemistry.reactions import reaction_workspace


def create_zcm_registry() -> ChemistryModuleRegistry:
    registry = ChemistryModuleRegistry()

    registry.register(element_catalog)
    registry.register(chemistry_calculator)
    registry.register(reaction_workspace)

    return registry


zcm_registry = create_zcm_registry()

__all__ = [
    "create_zcm_registry",
    "zcm_registry",
]
