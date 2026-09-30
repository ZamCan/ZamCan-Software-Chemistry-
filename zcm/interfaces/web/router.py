from __future__ import annotations

from typing import Any
from urllib.parse import unquote

from zcm.api.facade import zcm


def _property_payload(prop: Any) -> dict[str, Any]:
    return {
        "name": prop.name,
        "kind": prop.kind.value,
        "quantity": str(prop.quantity),
        "status": prop.status.value,
        "conditions": (
            prop.conditions.__dict__
            if prop.conditions is not None
            else None
        ),
        "uncertainty": (
            prop.uncertainty.__dict__
            if prop.uncertainty is not None
            else None
        ),
        "evidence": [
            {
                "type": evidence.evidence_type.value,
                "source": evidence.source,
                "reference": evidence.reference,
                "notes": evidence.notes,
            }
            for evidence in prop.evidence
        ],
        "notes": prop.notes,
    }


def system_payload() -> dict[str, Any]:
    return {
        "name": "ZamCan Software Chemistry",
        "short_name": "ZCS",
        "version": "0.1.0",
        "architecture": {
            "language_model": "LCM",
            "software_chemistry_model": "SCM",
            "application_model": "ZCM",
        },
        "modules": zcm.modules(),
        "capabilities": sorted(zcm.capabilities()),
    }


def elements_payload() -> list[dict[str, Any]]:
    elements = zcm.execute(
        "periodic_table",
        "all",
    )

    return [
        {
            "atomic_number": element.atomic_number,
            "name": element.name,
            "symbol": element.symbol,
            "period": element.period,
            "group": element.group,
            "block": element.block,
            "category": element.category.value,
            "property_count": len(element.properties),
        }
        for element in elements
    ]


def element_payload(identifier: str) -> dict[str, Any]:
    element = zcm.execute(
        "element_lookup",
        "get",
        unquote(identifier),
    )

    return {
        "atomic_number": element.atomic_number,
        "name": element.name,
        "symbol": element.symbol,
        "period": element.period,
        "group": element.group,
        "block": element.block,
        "category": element.category.value,
        "properties": [
            _property_payload(prop)
            for prop in element.properties
        ],
    }


def balance_reaction(
    reactants: list[str],
    products: list[str],
) -> dict[str, Any]:
    result = zcm.execute(
        "equation_balancing",
        "balance",
        reactants,
        products,
    )

    return {
        "equation": result.formatted(),
        "balanced": result.balanced,
        "reactant_coefficients": result.reactant_coefficients,
        "product_coefficients": result.product_coefficients,
    }


def assess_reaction(
    reactants: list[str],
    products: list[str] | None = None,
    conditions: list[str] | None = None,
) -> dict[str, Any]:
    result = zcm.execute(
        "reaction_assessment",
        "assess",
        reactants,
        products,
        tuple(conditions or ()),
    )

    return {
        "outcome": result.outcome.value,
        "reasons": [
            {
                "code": reason.code.value,
                "statement": reason.statement,
                "confidence": reason.confidence,
            }
            for reason in result.reasons
        ],
        "conditions": list(result.conditions),
    }
