"""Cross-check atom/ion/electron-state bookkeeping."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ElectronStateConsistency:
    atomic_number:int
    electron_count:int
    charge_number:int
    consistent:bool
    reason:str

def check_electron_state(atomic_number,electron_count,charge_number):
    if atomic_number<1 or electron_count<0: raise ValueError('invalid particle counts')
    expected=atomic_number-electron_count
    ok=expected==charge_number
    return ElectronStateConsistency(atomic_number,electron_count,charge_number,ok,'Z - e = charge' if ok else f'expected charge {expected}')
