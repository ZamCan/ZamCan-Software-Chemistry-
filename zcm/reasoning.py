"""Connect the SCM analytical planner to the existing ZCM calculations."""
from math import isfinite

from scm.chemistry.analytical.planning import plan_concentration
from scm.core import Quantity
from scm.core.units import get_unit
from zcm.calculations import calculate_dilution, calculate_mass_molarity, calculate_molarity, titrate


_QUANTITY_UNITS = {
    "amount": "mol",
    "mass": "g",
    "final_volume": "L",
    "stock": "mol/L",
    "aliquot": "L",
}
_TEXT_FIELDS = {"formula", "equation", "titrant", "analyte"}


def _quantity(data: object, expected_unit: str) -> Quantity:
    if not isinstance(data, dict) or set(data) != {"value", "unit"}:
        raise ValueError("A quantity must contain value and unit.")
    if not isinstance(data["unit"], str) or not data["unit"].strip():
        raise ValueError("A quantity unit must be nonempty text.")
    quantity = Quantity(_number(data["value"]), data["unit"])
    if quantity.dimension != get_unit(expected_unit).dimension:
        raise ValueError(f"Expected a unit compatible with {expected_unit}.")
    return quantity


def _number(value: object) -> float:
    if type(value) not in (float, int) or not isfinite(value):
        raise ValueError("Expected a finite number.")
    return value


def _text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected nonempty text.")
    return value.strip()


def infer_concentration(evidence: dict) -> dict:
    """Resolve one concentration problem with a trace of the route selection."""
    if not isinstance(evidence, dict) or any(not isinstance(key, str) for key in evidence):
        return {"status": "invalid_input", "message": "Evidence must be an object with text field names."}

    plan = plan_concentration(set(evidence))
    response = {"goal": "molar_concentration", **plan}
    if plan["status"] in ("invalid_input", "conflicting_evidence"):
        return response

    normalized = {}
    for field, value in evidence.items():
        try:
            if field in _QUANTITY_UNITS:
                normalized[field] = _quantity(value, _QUANTITY_UNITS[field])
            elif field in _TEXT_FIELDS:
                normalized[field] = _text(value)
            else:
                normalized[field] = _number(value)
        except (ValueError, OverflowError) as exc:
            return {**response, "status": "invalid_input", "field": field, "message": str(exc)}

    if plan["status"] != "ready":
        return response

    try:
        route = plan["route"]
        if route == "amount":
            result = calculate_molarity(**normalized)
        elif route == "mass":
            result = calculate_mass_molarity(**normalized)
        elif route == "dilution":
            result = calculate_dilution(**normalized)
        else:
            result = titrate(**normalized)
    except (ValueError, ArithmeticError) as exc:
        return {**response, "status": "invalid_input", "message": str(exc)}
    return {**response, "status": "calculated", "calculation": result}
