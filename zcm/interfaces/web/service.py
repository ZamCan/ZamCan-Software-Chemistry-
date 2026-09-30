from __future__ import annotations

from typing import Any

from .router import (
    assess_reaction,
    balance_reaction,
    element_payload,
    elements_payload,
    system_payload,
)


class ZCSService:
    """
    Application service boundary between HTTP transport
    and the ZCM/SCM scientific engines.
    """

    def system(self) -> dict[str, Any]:
        return system_payload()

    def elements(self) -> list[dict[str, Any]]:
        return elements_payload()

    def element(self, identifier: str) -> dict[str, Any]:
        return element_payload(identifier)

    def balance_reaction(
        self,
        reactants: list[str],
        products: list[str],
    ) -> dict[str, Any]:
        return balance_reaction(
            reactants,
            products,
        )

    def assess_reaction(
        self,
        reactants: list[str],
        products: list[str] | None = None,
        conditions: list[str] | None = None,
    ) -> dict[str, Any]:
        return assess_reaction(
            reactants,
            products,
            conditions,
        )


zcs_service = ZCSService()
