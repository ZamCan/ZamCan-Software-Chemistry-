from enum import Enum


class ElementCategory(str, Enum):
    ALKALI_METAL = "alkali_metal"
    ALKALINE_EARTH_METAL = "alkaline_earth_metal"
    TRANSITION_METAL = "transition_metal"
    POST_TRANSITION_METAL = "post_transition_metal"
    METALLOID = "metalloid"
    NONMETAL = "nonmetal"
    HALOGEN = "halogen"
    NOBLE_GAS = "noble_gas"
    LANTHANIDE = "lanthanide"
    ACTINIDE = "actinide"
    UNKNOWN = "unknown"


__all__ = [
    "ElementCategory",
]
