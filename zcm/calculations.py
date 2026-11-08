"""Structured, reproducible results for product-facing calculations."""
from dataclasses import asdict
from fractions import Fraction
from math import isfinite

from lcm import interpret, parse
from lcm.intent import IntentKind
from scm.core import Quantity, QuantityRange
from zcm.chemistry.molar_mass import molar_mass_workspace
from zcm.chemistry_api import ChemistryAPI


def _quantity_payload(quantity, unit):
    if isinstance(quantity, QuantityRange):
        return {
            "minimum": _quantity_payload(quantity.minimum, unit)["value"],
            "maximum": _quantity_payload(quantity.maximum, unit)["value"],
        }
    return {"value": quantity.value if quantity.unit == unit else quantity.to(unit).value}


def calculate(query: str) -> dict:
    """Route a supported chemical query through LCM and SCM."""
    intent = parse(query)
    if intent.kind not in (IntentKind.MOLAR_MASS, IntentKind.BALANCE_EQUATION):
        raise ValueError("Use 'molar mass FORMULA' or 'balance REACTANTS -> PRODUCTS'.")
    result = interpret(intent).result
    if intent.kind is IntentKind.MOLAR_MASS:
        return {
            "method": "composition_molar_mass",
            "status": "calculated",
            "input": {"formula": intent.target},
            "unit": "g/mol",
            "result": _quantity_payload(result.molar_mass, "g/mol"),
            "contributions": [
                {
                    "element": term.element,
                    "count": term.count,
                    **_quantity_payload(term.contribution, "g/mol"),
                    "atomic_weight_uncertainty": (
                        asdict(term.atomic_weight_uncertainty) if term.atomic_weight_uncertainty else None
                    ),
                    "references": [
                        {"source": evidence.source, "reference": evidence.reference}
                        for evidence in term.evidence
                    ],
                }
                for term in result.terms
            ],
        }
    return {
        "method": "equation_balancing",
        "status": "calculated" if result.balanced else "unbalanced",
        "input": {"reactants": list(intent.reactants), "products": list(intent.products)},
        "equation": result.formatted(),
        "reactant_coefficients": list(result.reactant_coefficients),
        "product_coefficients": list(result.product_coefficients),
    }


def titrate(
    titrant_mol_l: float, titrant_ml: float, analyte_ml: float, ratio: float | None = None,
    *, equation: str | None = None, titrant: str | None = None, analyte: str | None = None,
) -> dict:
    """Calculate analyte amount from an explicit or equation-derived ratio."""
    reaction = {}
    if equation is not None:
        if ratio is not None:
            raise ValueError("Supply either a mole ratio or a reaction equation.")
        if not titrant or not analyte or titrant == analyte:
            raise ValueError("Name distinct titrant and analyte reactants for the equation.")
        balanced = calculate(f"balance {equation}")
        reactants = balanced["input"]["reactants"]
        if len(reactants) != 2 or set(reactants) != {titrant, analyte}:
            raise ValueError("The titration equation must have the titrant and analyte as its two reactants.")
        coefficients = dict(zip(reactants, balanced["reactant_coefficients"], strict=True))
        exact_ratio = Fraction(coefficients[analyte], coefficients[titrant])
        ratio = float(exact_ratio)
        reaction = {
            "equation": balanced["equation"],
            "titrant": titrant,
            "analyte": analyte,
            "exact_mole_ratio": str(exact_ratio),
        }
    elif titrant is not None or analyte is not None:
        raise ValueError("Titrant and analyte formulas require a reaction equation.")
    if ratio is None:
        ratio = 1
    inputs = {
        "titrant_mol_l": titrant_mol_l,
        "titrant_ml": titrant_ml,
        "analyte_ml": analyte_ml,
        "analyte_moles_per_titrant_mole": ratio,
    }
    if any(isinstance(value, bool) or not isfinite(value) or value <= 0 for value in inputs.values()):
        raise ValueError("Titration inputs must be finite and positive.")
    result = ChemistryAPI.titration_from_quantities(
        Quantity(titrant_mol_l, "mol/L"), Quantity(titrant_ml, "mL"),
        Quantity(analyte_ml, "mL"), ratio,
    )
    return {
        "method": "equivalence_point_stoichiometry",
        "status": "calculated",
        "input": {**inputs, **reaction},
        "analyte_amount_mol": result.moles,
        "analyte_concentration_mol_l": result.concentration,
    }


def stoichiometry(equation: str, amounts_mol: dict) -> dict:
    """Calculate theoretical yields for a balanced, single reaction."""
    balanced = calculate(f"balance {equation}")
    if balanced["status"] != "calculated":
        raise ValueError("The reaction could not be balanced.")
    reactants = balanced["input"]["reactants"]
    products = balanced["input"]["products"]
    species = reactants + products
    if len(set(species)) != len(species):
        raise ValueError("Each formula must occur only once across the equation.")
    if not isinstance(amounts_mol, dict) or set(amounts_mol) != set(reactants):
        raise ValueError("Supply initial mol amounts for exactly the reactants in the equation.")
    amounts = {}
    for formula in reactants:
        value = amounts_mol[formula]
        if isinstance(value, bool) or not isinstance(value, (str, int, float, Fraction)):
            raise ValueError(f"Invalid mol amount for {formula}.")
        amount = Fraction(str(value))
        if amount < 0:
            raise ValueError(f"Mol amount for {formula} must be nonnegative.")
        amounts[formula] = amount

    coefficients = dict(zip(
        species, balanced["reactant_coefficients"] + balanced["product_coefficients"], strict=True
    ))
    result = ChemistryAPI.stoichiometry(amounts, dict.fromkeys(products, 0), coefficients)
    return {
        "method": "single_reaction_theoretical_yield",
        "status": "calculated",
        "assumption": "Complete conversion at the maximum stoichiometric extent.",
        "equation": balanced["equation"],
        "unit": "mol",
        "initial_amounts": {key: str(value) for key, value in amounts.items()},
        "extent": str(result.extent),
        "limiting_reactants": list(result.limiting_reactants),
        "consumed": {key: str(value) for key, value in result.consumed.items()},
        "produced": {key: str(value) for key, value in result.produced.items()},
        "remaining": {key: str(value) for key, value in result.excess_remaining.items()},
    }


def calculate_molarity(amount: Quantity, final_volume: Quantity) -> dict:
    result = ChemistryAPI.molarity(amount, final_volume)
    return _concentration_result(
        "amount_per_solution_volume", result, amount=amount, final_volume=final_volume
    )


def calculate_mass_molarity(formula: str, mass: Quantity, final_volume: Quantity) -> dict:
    molar_mass = molar_mass_workspace.calculate(formula).molar_mass
    result = ChemistryAPI.molarity_from_mass(mass, molar_mass, final_volume)
    return {
        **_concentration_result(
            "mass_via_molar_mass_per_solution_volume", result, mass=mass, final_volume=final_volume
        ),
        "formula": formula,
        "molar_mass": {"unit": "g/mol", **_quantity_payload(molar_mass, "g/mol")},
        "assumption": "The recorded mass is pure solute of the specified formula.",
    }


def calculate_dilution(stock: Quantity, aliquot: Quantity, final_volume: Quantity) -> dict:
    result = ChemistryAPI.diluted_molarity(stock, aliquot, final_volume)
    return _concentration_result(
        "dilution_with_conserved_solute", result, stock=stock, aliquot=aliquot, final_volume=final_volume
    )


def _concentration_result(method: str, result: Quantity | QuantityRange, **inputs: Quantity) -> dict:
    return {
        "method": method,
        "status": "calculated",
        "input": {
            name: {"value": quantity.value, "unit": quantity.unit}
            for name, quantity in inputs.items()
        },
        "unit": "mol/L",
        "result": _quantity_payload(result, "mol/L"),
    }
