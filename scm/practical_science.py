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


# SI inputs and outputs; assumptions are exposed with every result.
from math import exp, pi, log10
from types import MappingProxyType

@dataclass(frozen=True)
class Formula:
    inputs: tuple
    output_unit: str
    equation: str
    assumptions: str
    operation: object

def nonnegative(x):
    x = finite(x)
    if x < 0:
        raise ValueError("Nonnegative quantity required")
    return x

FORMULAS = MappingProxyType({
    "density": Formula(("mass_kg","volume_m3"),"kg/m^3","m/V","Homogeneous bulk density",density_kg_m3),
    "amount": Formula(("mass_kg","molar_mass_kg_mol"),"mol","m/M","Known chemical identity",lambda m,M: nonnegative(m)/positive(M)),
    "molarity": Formula(("amount_mol","solution_volume_m3"),"mol/m^3","n/V","Final solution volume",lambda n,V: nonnegative(n)/positive(V)),
    "molality": Formula(("amount_mol","solvent_mass_kg"),"mol/kg","n/m","Solvent mass, not solution mass",lambda n,m: nonnegative(n)/positive(m)),
    "ideal_gas_pressure": Formula(("amount_mol","temperature_k","volume_m3"),"Pa","nRT/V","Ideal gas approximation",lambda n,T,V: nonnegative(n)*R*positive(T)/positive(V)),
    "ideal_gas_volume": Formula(("amount_mol","temperature_k","pressure_pa"),"m^3","nRT/P","Ideal gas approximation",lambda n,T,P: nonnegative(n)*R*positive(T)/positive(P)),
    "ph": Formula(("hydrogen_activity",),"1","-log10(a_H+)","Dimensionless hydrogen ion activity",lambda a: -log10(positive(a))),
    "gibbs_energy": Formula(("enthalpy_j_mol","temperature_k","entropy_j_mol_k"),"J/mol","H-TS","Consistent thermodynamic states",lambda H,T,S: H-positive(T)*S),
    "arrhenius_rate": Formula(("prefactor","activation_energy_j_mol","temperature_k"),"same as prefactor","A exp(-Ea/RT)","Arrhenius model",lambda A,E,T: nonnegative(A)*exp(-E/(R*positive(T)))),
    "force": Formula(("mass_kg","acceleration_m_s2"),"N","ma","Constant mass, inertial frame",lambda m,a: nonnegative(m)*a),
    "kinetic_energy": Formula(("mass_kg","speed_m_s"),"J","mv^2/2","Nonrelativistic motion",lambda m,v: nonnegative(m)*nonnegative(v)**2/2),
    "momentum": Formula(("mass_kg","velocity_m_s"),"kg m/s","mv","One-dimensional nonrelativistic motion",lambda m,v: nonnegative(m)*v),
    "pressure": Formula(("normal_force_n","area_m2"),"Pa","F/A","Average normal pressure",lambda F,A: nonnegative(F)/positive(A)),
    "hydrostatic_pressure": Formula(("density_kg_m3","gravity_m_s2","depth_m"),"Pa","rho g h","Constant density and gravity; gauge pressure",lambda d,g,h: nonnegative(d)*positive(g)*nonnegative(h)),
    "sensible_heat": Formula(("mass_kg","specific_heat_j_kg_k","delta_temperature_k"),"J","mc deltaT","Constant specific heat; no phase transition",lambda m,c,T: nonnegative(m)*positive(c)*T),
    "latent_heat": Formula(("mass_kg","specific_latent_heat_j_kg"),"J","mL","Specified phase transition",lambda m,L: nonnegative(m)*positive(L)),
    "ohm_voltage": Formula(("current_a","resistance_ohm"),"V","IR","Ohmic element",lambda I,R: I*nonnegative(R)),
    "electric_power": Formula(("voltage_v","current_a"),"W","VI","DC or instantaneous power",lambda V,I: V*I),
    "wave_speed": Formula(("frequency_hz","wavelength_m"),"m/s","f lambda","Phase velocity",lambda f,w: positive(f)*positive(w)),
    "photon_energy": Formula(("frequency_hz",),"J","hf","Single photon",lambda f: CONSTANTS["planck"].value*positive(f)),
    "radioactive_remaining": Formula(("initial_amount","elapsed_s","half_life_s"),"same as initial amount","N0 2^(-t/t_half)","Single exponential decay",lambda N,t,h: nonnegative(N)*2**(-nonnegative(t)/positive(h))),
    "faraday_amount": Formula(("charge_c","electrons_per_formula_unit"),"mol","Q/(zF)","100 percent current efficiency",lambda Q,z: nonnegative(Q)/(positive(z)*CONSTANTS["avogadro"].value*CONSTANTS["elementary_charge"].value)),
})

def calculate(name, **quantities):
    formula = FORMULAS[name]
    if set(quantities) != set(formula.inputs):
        raise ValueError("Required SI inputs: " + ", ".join(formula.inputs))
    value = finite(formula.operation(*(finite(quantities[k]) for k in formula.inputs)))
    return {"value": value, "unit": formula.output_unit, "equation": formula.equation,
            "assumptions": formula.assumptions, "status": "calculated"}

# Additional SI relationships, kept separate from the immutable initial registry.
FORMULAS = MappingProxyType({**FORMULAS,
    "mass_fraction": Formula(("solute_mass_kg","solution_mass_kg"),"1","m_solute/m_solution","Mass fraction between zero and one",lambda m,M: fraction(m,M)),
    "dilution_volume": Formula(("initial_concentration","initial_volume_m3","final_concentration"),"m^3","C1 V1/C2","Conserved solute; dilution only",lambda c,v,C: dilution(c,v,C)),
    "percent_yield": Formula(("actual_mass_kg","theoretical_mass_kg"),"%","100 actual/theoretical","Apparent yield may exceed 100 percent; check purity",lambda a,t: 100*nonnegative(a)/positive(t)),
    "gravitational_energy": Formula(("mass_kg","gravity_m_s2","height_change_m"),"J","mgh","Uniform gravitational field",lambda m,g,h: nonnegative(m)*positive(g)*h),
    "acceleration": Formula(("initial_velocity_m_s","final_velocity_m_s","elapsed_s"),"m/s^2","(v-u)/t","Average acceleration",lambda u,v,t:(v-u)/positive(t)),
    "displacement": Formula(("initial_velocity_m_s","acceleration_m_s2","elapsed_s"),"m","ut+at^2/2","Constant acceleration",lambda u,a,t:u*nonnegative(t)+a*t*t/2),
    "centripetal_acceleration": Formula(("speed_m_s","radius_m"),"m/s^2","v^2/r","Circular motion",lambda v,r:nonnegative(v)**2/positive(r)),
    "spring_energy": Formula(("spring_constant_n_m","extension_m"),"J","kx^2/2","Linear elastic spring",lambda k,x:positive(k)*x*x/2),
    "electrical_energy": Formula(("power_w","elapsed_s"),"J","Pt","Constant power",lambda P,t:P*nonnegative(t)),
    "resistivity_resistance": Formula(("resistivity_ohm_m","length_m","area_m2"),"ohm","rho L/A","Uniform conductor at specified temperature",lambda r,L,A:nonnegative(r)*positive(L)/positive(A)),
    "capacitor_energy": Formula(("capacitance_f","voltage_v"),"J","CV^2/2","Linear capacitor",lambda C,V:positive(C)*V*V/2),
    "refractive_index": Formula(("phase_speed_m_s",),"1","c/v","Phase refractive index",lambda v:CONSTANTS["light_speed"].value/positive(v)),
    "frequency_period": Formula(("period_s",),"Hz","1/T","Periodic signal",lambda t:1/positive(t)),
    "buoyant_force": Formula(("fluid_density_kg_m3","displaced_volume_m3","gravity_m_s2"),"N","rho V g","Uniform fluid density",lambda d,V,g:nonnegative(d)*nonnegative(V)*positive(g)),
    "heat_power": Formula(("energy_j","elapsed_s"),"W","Q/t","Average heat transfer rate",lambda Q,t:Q/positive(t)),
    "osmotic_pressure": Formula(("vant_hoff_factor","concentration_mol_m3","temperature_k"),"Pa","iCRT","Ideal dilute solution",lambda i,c,T:positive(i)*nonnegative(c)*R*positive(T)),
    "first_order_remaining": Formula(("initial_concentration","rate_constant_s_inv","elapsed_s"),"same as initial concentration","C0 exp(-kt)","First-order irreversible reaction",lambda C,k,t:nonnegative(C)*exp(-nonnegative(k)*nonnegative(t))),
})

def fraction(m,M):
    result=nonnegative(m)/positive(M)
    if result>1:
        raise ValueError("Solute mass exceeds solution mass")
    return result

def dilution(c,v,C):
    c,C=positive(c),positive(C)
    if C>c:
        raise ValueError("Final concentration exceeds initial concentration")
    return c*positive(v)/C

def formula_catalog():
    return {name: {"inputs": list(f.inputs), "unit": f.output_unit,
                   "equation": f.equation, "assumptions": f.assumptions}
            for name,f in FORMULAS.items()}

def constants_catalog():
    from dataclasses import asdict
    return {**{k:asdict(v) for k,v in CONSTANTS.items()},
            "gas_constant":asdict(Constant(R,"J/(mol K)",True,"Derived from exact SI constants")),
            "faraday":asdict(Constant(CONSTANTS["avogadro"].value*CONSTANTS["elementary_charge"].value,"C/mol",True,"Derived from exact SI constants"))}
