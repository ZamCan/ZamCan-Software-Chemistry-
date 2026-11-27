"""Condition-aware scientific reasoning; no experimental claims inferred."""
from dataclasses import dataclass
from math import isfinite, log, fsum, hypot
from scm.scientific_validation import conservation_residual

R = 8.31446261815324
SOURCE = "https://doi.org/10.1351/goldbook.C01023"

@dataclass(frozen=True)
class Evidence:
    source: str
    version: str
    origin: str
    def __post_init__(self):
        if not self.source.strip() or not self.version.strip():
            raise ValueError("Source and version required")
        if self.origin not in {"experimental", "analytical", "computational", "prediction", "hypothesis"}:
            raise ValueError("Unknown evidence origin")

def equilibrium_reasoning(reactants, products, delta_g_standard, temperature, activities, coefficients, evidence, tolerance_j=1e-6):
    """J/mol, K, dimensionless positive activities, signed stoichiometry.
    Caller supplies matching species identities and standard-state conventions.
    """
    if not isinstance(evidence, Evidence):
        raise ValueError("Evidence required")
    if not isfinite(temperature) or temperature <= 0 or not isfinite(delta_g_standard):
        raise ValueError("Invalid thermodynamic inputs")
    if not isfinite(tolerance_j) or tolerance_j < 0:
        raise ValueError("Invalid numerical tolerance")
    residual = conservation_residual(reactants, products)
    if residual["atoms"] or residual["charge"]:
        return {"status": "rejected", "reason": "conservation_failed", "residual": residual}
    if set(activities) != set(coefficients) or not coefficients:
        raise ValueError("Matching activities and coefficients required")
    if any(not isfinite(a) or a <= 0 for a in activities.values()):
        raise ValueError("Positive finite activities required")
    if any(not isfinite(v) or v == 0 for v in coefficients.values()) or not any(v < 0 for v in coefficients.values()) or not any(v > 0 for v in coefficients.values()):
        raise ValueError("Signed reactant and product coefficients required")
    log_q = fsum(coefficients[k] * log(a) for k,a in activities.items())
    dg = delta_g_standard + R * temperature * log_q
    if not isfinite(dg):
        raise ValueError("Nonfinite result")
    direction = "near_equilibrium" if abs(dg) <= tolerance_j else ("forward" if dg < 0 else "reverse")
    return {"status": "calculated", "direction": direction, "delta_g_j_mol": dg,
            "log_q": log_q, "log_k": -delta_g_standard/(R*temperature),
            "source": SOURCE, "evidence": evidence, "temperature_k": temperature,
            "limitations": "Thermodynamic tendency only; rate, mechanism and experimental feasibility not established."}

def compare_properties(a, b):
    """Compare records only at identical identity, units, property and conditions."""
    keys = ("identity", "property", "unit", "conditions")
    if any(k not in a or k not in b for k in keys):
        raise ValueError("Missing comparison metadata")
    if any(a[k] != b[k] for k in keys):
        return {"status": "incomparable"}
    if not all(isinstance(x.get("evidence"), Evidence) for x in (a,b)):
        raise ValueError("Evidence required")
    if not all(isfinite(x["value"]) for x in (a,b)):
        raise ValueError("Invalid property value")
    difference = a["value"]-b["value"]
    if not isfinite(difference):
        raise ValueError("Nonfinite difference")
    uncertainties = [x.get("standard_uncertainty") for x in (a,b)]
    if any(u is not None and (not isfinite(u) or u < 0) for u in uncertainties):
        raise ValueError("Invalid uncertainty")
    combined = hypot(*uncertainties) if all(u is not None for u in uncertainties) else None
    return {"status": "compared", "difference": difference, "unit": a["unit"],
            "combined_standard_uncertainty": combined,
            "assumption": "Independent standard uncertainties; no inference of experimental confirmation."}
