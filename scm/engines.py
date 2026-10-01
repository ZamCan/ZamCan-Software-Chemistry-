from dataclasses import dataclass
import math

@dataclass(frozen=True)
class EquilibriumResult:
    quotient: float
    status: str = 'calculated'

def reaction_quotient(products, reactants, product_powers=None, reactant_powers=None):
    pp=product_powers or {k:1 for k in products}; rp=reactant_powers or {k:1 for k in reactants}
    if any(v<=0 for v in products.values()) or any(v<=0 for v in reactants.values()): raise ValueError('activities must be positive')
    return EquilibriumResult(math.prod(products[k]**pp[k] for k in products)/math.prod(reactants[k]**rp[k] for k in reactants))

@dataclass(frozen=True)
class TitrationResult:
    moles: float
    concentration: float

def titration(titrant_molarity, titrant_volume_l, analyte_volume_l, ratio=1.0):
    if analyte_volume_l<=0 or min(titrant_molarity,titrant_volume_l,ratio)<0: raise ValueError('invalid titration inputs')
    m=titrant_molarity*titrant_volume_l*ratio
    return TitrationResult(m,m/analyte_volume_l)

@dataclass(frozen=True)
class Stream:
    name: str
    components: dict[str,float]

@dataclass(frozen=True)
class MaterialBalance:
    residual: dict[str,float]
    balanced: bool

def material_balance(inlets, outlets, tolerance=1e-9):
    ins={}; outs={}
    for s in inlets:
        for k,v in s.components.items(): ins[k]=ins.get(k,0)+v
    for s in outlets:
        for k,v in s.components.items(): outs[k]=outs.get(k,0)+v
    residual={k:ins.get(k,0)-outs.get(k,0) for k in set(ins)|set(outs)}
    return MaterialBalance(residual,all(abs(v)<=tolerance for v in residual.values()))
