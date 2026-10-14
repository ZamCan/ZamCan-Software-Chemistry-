"""Shared validation primitives for scientific inputs and derived outputs."""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Iterable

@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = 'error'
    path: str | None = None

@dataclass(frozen=True)
class ValidationReport:
    issues: tuple[ValidationIssue, ...]
    @property
    def valid(self) -> bool:
        return not any(i.severity == 'error' for i in self.issues)
    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(i for i in self.issues if i.severity == 'warning')

def finite_number(value: object, name: str, *, minimum: float | None = None, strict_minimum: bool = False) -> tuple[ValidationIssue, ...]:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        return (ValidationIssue('not_finite_number', f'{name} must be a finite real number', path=name),)
    if minimum is not None and (value <= minimum if strict_minimum else value < minimum):
        op = 'greater than' if strict_minimum else 'at least'
        return (ValidationIssue('out_of_range', f'{name} must be {op} {minimum}', path=name),)
    return ()

def validate_unique(values: Iterable[str], name: str = 'values') -> ValidationReport:
    seen=set(); issues=[]
    for index, value in enumerate(values):
        if value in seen: issues.append(ValidationIssue('duplicate_value', f'duplicate {name}: {value}', path=f'{name}[{index}]'))
        seen.add(value)
    return ValidationReport(tuple(issues))
