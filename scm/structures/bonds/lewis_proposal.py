"""Auditable Lewis-structure candidate generation.
This proposes electron bookkeeping only when the caller supplies atom order and connectivity; it never claims quantum-mechanical uniqueness.
"""
from dataclasses import dataclass
@dataclass(frozen=True)
class LewisCandidate:
    bond_orders:tuple[float,...]
    lone_pairs:tuple[int,...]
    formal_charges:tuple[int,...]
    score:float
    rationale:tuple[str,...]

def propose_lone_pairs(valence_electrons,bond_order_sums,net_charge=0):
    if len(valence_electrons)!=len(bond_order_sums): raise ValueError('length mismatch')
    total=sum(valence_electrons)-net_charge
    if total<0: raise ValueError('electron budget is negative')
    remaining=total-2*sum(bond_order_sums)
    if remaining<0 or remaining%2: return ()
    pairs=[0]*len(valence_electrons)
    # Conservative baseline: allocate available pairs to satisfy duet/octet where possible.
    for i,(v,b) in enumerate(zip(valence_electrons,bond_order_sums)):
        target=2 if v<=2 else 8
        need=max(0,target-2*b)
        pairs[i]=need//2
    if sum(pairs)*2>remaining: return ()
    return tuple(pairs)
