"""Analytical everyday chemistry primitives with explicit applicability."""
from math import isfinite, log10

def positive(x, name):
    if not isfinite(x) or x <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return x

def dilution(initial_mol_l, initial_l, final_l):
    positive(initial_l, "initial volume")
    positive(final_l, "final volume")
    if final_l < initial_l or not isfinite(initial_mol_l) or initial_mol_l < 0:
        raise ValueError("Invalid dilution inputs")
    return {"value": initial_mol_l * (initial_l / final_l), "unit":"mol/L",
            "origin":"analytical", "assumptions":["Conserved solute amount", "Known final volume", "No reaction or precipitation"]}

def ph_from_activity(activity):
    positive(activity, "hydrogen ion activity")
    return {"value":-log10(activity), "unit":"1", "origin":"analytical",
            "assumptions":["Dimensionless hydrogen ion activity supplied; not concentration"]}

def hardness_as_caco3(calcium_mg_l, magnesium_mg_l):
    if any(not isfinite(x) or x < 0 for x in (calcium_mg_l, magnesium_mg_l)):
        raise ValueError("Nonnegative finite concentrations required")
    value = calcium_mg_l * 100.0869/40.078 + magnesium_mg_l * 100.0869/24.305
    if not isfinite(value):
        raise ValueError("Nonfinite result")
    return {"value":value,"unit":"mg/L as CaCO3","origin":"analytical",
            "assumptions":["Calcium and magnesium contributions only"],
            "limitations":"Does not establish drinking-water safety."}

def electrical_energy(voltage_v, current_a, seconds):
    if any(not isfinite(x) or x < 0 for x in (voltage_v,current_a,seconds)):
        raise ValueError("Nonnegative finite inputs required")
    value = voltage_v * current_a * seconds
    if not isfinite(value):
        raise ValueError("Nonfinite result")
    return {"value":value,"unit":"J","origin":"analytical",
            "assumptions":["Constant voltage and current magnitudes"],
            "limitations":"Does not predict battery capacity or chemical efficiency."}
