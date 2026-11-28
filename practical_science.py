"""Standalone practical science foundations; integration and validation pending."""
from dataclasses import dataclass
from math import isfinite, sqrt, fsum, log10, floor
from statistics import stdev

def finite(x):
    x = float(x)
    if not isfinite(x):
        raise ValueError("Nonfinite quantity")
    return x

def positive(x):
    x = finite(x)
    if x <= 0:
        raise ValueError("Positive quantity required")
    return x

@dataclass(frozen=True)
class Constant:
    value: float
    unit: str
    exact: bool
    source: str

CONSTANTS = {
    "avogadro": Constant(6.02214076e23, "mol^-1", True, "SI 2019"),
    "boltzmann": Constant(1.380649e-23, "J/K", True, "SI 2019"),
    "planck": Constant(6.62607015e-34, "J s", True, "SI 2019"),
    "light_speed": Constant(299792458, "m/s", True, "SI"),
    "elementary_charge": Constant(1.602176634e-19, "C", True, "SI 2019"),
    "standard_atmosphere": Constant(101325, "Pa", True, "standard atmosphere definition"),
    "standard_gravity": Constant(9.80665, "m/s^2", True, "conventional standard gravity"),
}
R = CONSTANTS["avogadro"].value * CONSTANTS["boltzmann"].value

@dataclass(frozen=True)
class Conditions:
    temperature_k: float | None = None
    pressure_pa: float | None = None
    def __post_init__(self):
        for x in (self.temperature_k, self.pressure_pa):
            if x is not None:
                positive(x)
    def require(self):
        if self.temperature_k is None or self.pressure_pa is None:
            raise ValueError("Temperature and pressure must be specified")
        return self.temperature_k, self.pressure_pa

def density_kg_m3(mass_kg, volume_m3):
    mass = finite(mass_kg)
    if mass < 0:
        raise ValueError("Negative mass")
    return mass / positive(volume_m3)

def ideal_gas_molar_volume_m3(conditions):
    t, p = conditions.require()
    return R*t/p

def measurement_summary(values):
    xs = [finite(x) for x in values]
    if len(xs) < 2:
        raise ValueError("At least two observations required")
    s = stdev(xs)
    return {"n": len(xs), "mean": fsum(xs)/len(xs), "sample_sd": s,
            "standard_error": s/sqrt(len(xs)),
            "assumption": "Independent observations; systematic error not included"}

def significant_figures(value, digits):
    x = finite(value)
    if not isinstance(digits, int) or isinstance(digits, bool) or not 1 <= digits <= 15:
        raise ValueError("Digits must be an integer from 1 to 15")
    return format(x, f".{digits}g")

def negligibility(omitted_error_bound, reference_magnitude, tolerance):
    error = finite(omitted_error_bound)
    tol = positive(tolerance)
    if error < 0 or tol > 1:
        raise ValueError("Invalid error bound or relative tolerance")
    ratio = error / positive(abs(finite(reference_magnitude)))
    return {"relative_error_bound": ratio, "tolerance": tol,
            "negligible": ratio <= tol,
            "assumption": "Supplied bound applies to final result"}

@dataclass(frozen=True)
class Observation:
    test: str
    observation: str
    inference: str
    evidence_status: str = "unverified"
    def __post_init__(self):
        if self.evidence_status not in ("unverified", "observed", "calculated", "predicted"):
            raise ValueError("Invalid evidence status")

def qualitative_sheet(sample_id, observations, profile="general"):
    if profile not in ("general", "necta_draft"):
        raise ValueError("Unknown profile")
    return {"sample_id": sample_id, "profile": profile,
            "official_format_verified": False,
            "rows": [{"test": o.test, "observation": o.observation,
                      "inference": o.inference, "evidence_status": o.evidence_status}
                     for o in observations],
            "conclusion": None}
