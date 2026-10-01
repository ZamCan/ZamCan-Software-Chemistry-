from dataclasses import dataclass, field

@dataclass
class Formulation:
    name:str
    ingredients:dict[str,float]
    basis:str='mass'
    notes:list[str]=field(default_factory=list)
    def total(self): return sum(self.ingredients.values())
    def fractions(self):
        t=self.total()
        return {k:v/t for k,v in self.ingredients.items()} if t else {}
