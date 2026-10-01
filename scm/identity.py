"""Canonical chemical identity keys independent of display names."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ChemicalIdentity:
    composition:tuple[tuple[str,int],...]
    charge:int=0
    radical:bool=False
    isotope_signature:tuple[tuple[str,int],...]=()
    def key(self):
        return (tuple(sorted(self.composition)),self.charge,self.radical,tuple(sorted(self.isotope_signature)))

def identity_equal(a,b): return a.key()==b.key()
