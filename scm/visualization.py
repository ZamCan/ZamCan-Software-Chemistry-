from dataclasses import dataclass
from enum import Enum

class VisualLayer(str,Enum): NANO='nano'; MOLECULAR='molecular'; LABORATORY='laboratory'; PROCESS='process'; SENSOR='sensor'
@dataclass(frozen=True)
class VisualNode:
    node_id:str
    kind:str
    label:str
    properties:dict
@dataclass(frozen=True)
class VisualEdge:
    source:str
    target:str
    kind:str
    properties:dict
@dataclass(frozen=True)
class ScientificScene:
    layer:VisualLayer
    nodes:tuple[VisualNode,...]
    edges:tuple[VisualEdge,...]=()
    metadata:dict|None=None

def scene(layer,nodes,edges=(),metadata=None):
    return ScientificScene(layer,tuple(nodes),tuple(edges),metadata or {})
