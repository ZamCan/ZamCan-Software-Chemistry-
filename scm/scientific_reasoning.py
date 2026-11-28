"""Bounded deterministic reasoning over explicitly registered scientific relationships."""
from dataclasses import dataclass
from math import isclose, isfinite
from scm.practical_science import calculate, FORMULAS

@dataclass(frozen=True)
class Rule:
    formula: str
    output: str
    inputs: tuple

RULES = (
    Rule("amount","amount_mol",("mass_kg","molar_mass_kg_mol")),
    Rule("molarity","concentration_mol_m3",("amount_mol","solution_volume_m3")),
    Rule("density","density_kg_m3",("mass_kg","volume_m3")),
    Rule("ideal_gas_pressure","pressure_pa",("amount_mol","temperature_k","volume_m3")),
    Rule("ideal_gas_volume","volume_m3",("amount_mol","temperature_k","pressure_pa")),
    Rule("hydrostatic_pressure","gauge_pressure_pa",("density_kg_m3","gravity_m_s2","depth_m")),
    Rule("force","force_n",("mass_kg","acceleration_m_s2")),
    Rule("kinetic_energy","kinetic_energy_j",("mass_kg","speed_m_s")),
    Rule("ohm_voltage","voltage_v",("current_a","resistance_ohm")),
    Rule("electric_power","power_w",("voltage_v","current_a")),
    Rule("electrical_energy","electrical_energy_j",("power_w","elapsed_s")),
    Rule("frequency_period","frequency_hz",("period_s",)),
    Rule("photon_energy","photon_energy_j",("frequency_hz",)),
    Rule("wave_speed","wave_speed_m_s",("frequency_hz","wavelength_m")),
    Rule("osmotic_pressure","osmotic_pressure_pa",("vant_hoff_factor","concentration_mol_m3","temperature_k")),
)

def reason(target, known, allowed_formulas):
    """One physical system per call. Explicit model opt-in; no hidden defaults."""
    allowed = set(allowed_formulas)
    if allowed - set(FORMULAS):
        raise ValueError("Unknown formula")
    if len(known)>128:
        raise ValueError("Too many input quantities")
    values = {k:float(v) for k,v in known.items()}
    if not all(isfinite(v) for v in values.values()):
        raise ValueError("Nonfinite input")
    trace=[]
    conflicts=[]
    rejected=[]
    done=set()
    for _ in range(len(RULES)+1):
        changed=False
        for rule in RULES:
            if rule in done or rule.formula not in allowed or not all(k in values for k in rule.inputs):
                continue
            done.add(rule)
            try:
                result=calculate(rule.formula,**dict(zip(FORMULAS[rule.formula].inputs,(values[k] for k in rule.inputs))))
            except (ValueError,OverflowError,ZeroDivisionError) as exc:
                rejected.append({"formula":rule.formula,"reason":str(exc)})
                continue
            v=result["value"]
            if rule.output in values:
                if not isclose(values[rule.output],v,rel_tol=1e-9,abs_tol=0):
                    conflicts.append({"quantity":rule.output,"existing":values[rule.output],"derived":v})
            else:
                values[rule.output]=v
                changed=True
                trace.append({"output":rule.output,"formula":rule.formula,"inputs":{k:values[k] for k in rule.inputs},**result})
        if not changed:
            break
    missing=[{"formula":r.formula,"missing":[k for k in r.inputs if k not in values]} for r in RULES if r.output==target and r.formula in allowed]
    status="conflict" if conflicts else "available" if target in values else "insufficient_information"
    return {"status":status,"target":target,"value":values.get(target) if status=="available" else None,
            "trace":trace,"conflicts":conflicts,"rejected":rejected,"candidate_requirements":missing,
            "limitation":"Explicitly selected models; one system; no experimental verification or uncertainty propagation."}
