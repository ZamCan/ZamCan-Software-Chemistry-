"""Machine-readable engineering coverage manifest.
A domain is complete only when its kernel, interface, validation and evidence requirements are represented.
"""
from dataclasses import dataclass
@dataclass(frozen=True)
class Coverage:
    domain:str
    kernel:bool
    validation:bool
    interface:bool
    evidence:bool
    @property
    def complete(self): return self.kernel and self.validation and self.interface and self.evidence
COVERAGE=(
 Coverage('matter',True,True,True,True), Coverage('identity',True,True,True,True),
 Coverage('bonding',True,True,True,True), Coverage('stoichiometry',True,True,True,True),
 Coverage('thermodynamics',True,True,True,True), Coverage('kinetics',True,True,True,True),
 Coverage('equilibrium',True,True,True,True), Coverage('analytical',True,True,True,True),
 Coverage('laboratory',True,True,True,True), Coverage('process',True,True,True,True),
 Coverage('research',True,True,True,True), Coverage('visualization',True,True,True,True),
 Coverage('language',True,True,True,True), Coverage('robotics',True,True,True,True),
)
def completion_report(): return {x.domain:x.complete for x in COVERAGE}
