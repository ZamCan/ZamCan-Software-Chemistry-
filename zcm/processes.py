from dataclasses import dataclass, field

@dataclass
class ProcessStep:
    name:str
    inputs:dict[str,float]
    outputs:dict[str,float]
    conditions:dict[str,float|str]=field(default_factory=dict)

@dataclass
class ProcessModel:
    name:str
    steps:list[ProcessStep]=field(default_factory=list)
    def add(self,step): self.steps.append(step)
    def component_totals(self):
        total={}
        for s in self.steps:
            for k,v in s.outputs.items(): total[k]=total.get(k,0)+v
        return total
