"""Condition-aware property records with provenance and explicit conflicts."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

class PropertyLookupStatus(str, Enum): RESOLVED='resolved'; AMBIGUOUS='ambiguous'; NOT_FOUND='not_found'
@dataclass(frozen=True)
class PropertyRecord:
    subject: str
    name: str
    value: Any
    unit: str | None = None
    conditions: tuple[tuple[str, str], ...] = ()
    source: str = ''
    status: str = 'reference'
    uncertainty: Any = None
    @property
    def condition_map(self): return dict(self.conditions)
@dataclass(frozen=True)
class PropertyLookup:
    status: PropertyLookupStatus
    records: tuple[PropertyRecord, ...]
    explanation: str
class PropertyRegistry:
    def __init__(self): self._records=[]
    def add(self, record: PropertyRecord):
        if not record.subject or not record.name: raise ValueError('subject and property name are required')
        if len(dict(record.conditions)) != len(record.conditions): raise ValueError('duplicate condition keys')
        self._records.append(record)
    def lookup(self, subject: str, name: str, conditions: dict[str,str] | None = None) -> PropertyLookup:
        wanted={k.casefold():v.casefold() for k,v in (conditions or {}).items()}
        matches=[]
        for record in self._records:
            if record.subject.casefold()!=subject.casefold() or record.name.casefold()!=name.casefold(): continue
            available={k.casefold():v.casefold() for k,v in record.conditions}
            if all(available.get(k)==v for k,v in wanted.items()): matches.append(record)
        if not matches: return PropertyLookup(PropertyLookupStatus.NOT_FOUND,(), 'No matching property record under the requested conditions.')
        values={(repr(r.value),r.unit) for r in matches}
        if len(values)>1: return PropertyLookup(PropertyLookupStatus.AMBIGUOUS,tuple(matches),'Multiple distinct values match; inspect conditions, status and provenance.')
        return PropertyLookup(PropertyLookupStatus.RESOLVED,tuple(matches),'Matching record(s) share a value; provenance is retained.')
