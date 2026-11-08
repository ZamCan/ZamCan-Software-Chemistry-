"""Select a concentration calculation from explicit analytical evidence."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ConcentrationRoute:
    name: str
    required: tuple[str, ...]
    explanation: str


_TITRATION = ("titrant_mol_l", "titrant_ml", "analyte_ml")
_ROUTES = (
    ConcentrationRoute("amount", ("amount", "final_volume"), "Divide solute amount by final solution volume."),
    ConcentrationRoute(
        "mass", ("formula", "mass", "final_volume"),
        "Resolve molar mass from the formula, convert solute mass to amount, then divide by final solution volume.",
    ),
    ConcentrationRoute(
        "dilution", ("stock", "aliquot", "final_volume"),
        "Conserve the solute amount in the stock aliquot and divide by final solution volume.",
    ),
    ConcentrationRoute(
        "titration_ratio", (*_TITRATION, "ratio"),
        "Use the supplied analyte-to-titrant mole ratio at equivalence.",
    ),
    ConcentrationRoute(
        "titration_equation", (*_TITRATION, "equation", "titrant", "analyte"),
        "Balance the reaction and use its analyte-to-titrant coefficient ratio at equivalence.",
    ),
)
_FIELDS = frozenset(field for route in _ROUTES for field in route.required)


def plan_concentration(fields: set[str]) -> dict:
    """Return possible routes, missing fields and an executable route when unique."""
    unknown = sorted(fields - _FIELDS)
    if unknown:
        return {"status": "invalid_input", "unknown_fields": unknown, "candidates": []}

    candidates = [
        {
            "route": route.name,
            "used": [field for field in route.required if field in fields],
            "missing": [field for field in route.required if field not in fields],
            "reason": route.explanation,
        }
        for route in _ROUTES
        if fields.issubset(route.required)
    ]
    if not candidates:
        return {
            "status": "conflicting_evidence",
            "message": "The supplied fields do not describe a single supported calculation. Submit one evidence set per calculation.",
            "candidates": [],
        }

    if len(candidates) == 1 and not candidates[0]["missing"]:
        return {"status": "ready", "route": candidates[0]["route"], "candidates": candidates}

    return {
        "status": "needs_evidence",
        "message": "Supply the missing fields for one candidate calculation.",
        "candidates": candidates,
    }
