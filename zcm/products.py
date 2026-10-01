"""Product surfaces sharing the same SCM kernel; no duplicate chemistry logic."""
from dataclasses import dataclass, field

@dataclass
class ProductWorkspace:
    name:str
    mode:str
    records:list[dict]=field(default_factory=list)
    def add(self,**record): self.records.append(record)

EDUCATION=ProductWorkspace('ZCM Education','education')
LABORATORY=ProductWorkspace('ZCM Laboratory','laboratory')
RESEARCH=ProductWorkspace('ZCM Research','research')
INDUSTRIAL=ProductWorkspace('ZCM Industrial','industrial')
