"""Education product primitives backed by explicit calculations."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class WorkedStep:
    label: str
    expression: str
    result: Any
    units: str | None = None
    rationale: str = ''

@dataclass(frozen=True)
class WorkedSolution:
    problem: str
    answer: Any
    units: str | None
    steps: tuple[WorkedStep,...]
    assumptions: tuple[str,...] = ()
    limitations: tuple[str,...] = ()

def solution_from_steps(problem: str, steps: tuple[WorkedStep,...], *, assumptions=(), limitations=()) -> WorkedSolution:
    if not problem.strip(): raise ValueError('problem must not be empty')
    if not steps: raise ValueError('at least one computational step is required')
    last=steps[-1]
    return WorkedSolution(problem,last.result,last.units,steps,tuple(assumptions),tuple(limitations))
