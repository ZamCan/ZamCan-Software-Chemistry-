from dataclasses import dataclass
@dataclass(frozen=True)
class CompositionResult:
    components:tuple[tuple[str,float],...]
    total:float
    normalized:dict[str,float]
def normalize_composition(values):
    if not values or any(v<0 for v in values.values()): raise ValueError('values must be nonnegative')
    total=sum(values.values())
    if total<=0: raise ValueError('total must be positive')
    return CompositionResult(tuple(values.items()),total,{k:v/total for k,v in values.items()})
