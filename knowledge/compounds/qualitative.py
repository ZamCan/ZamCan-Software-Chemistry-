"""School-level qualitative signatures for single salts."""

REFERENCE = "https://www.aqa.org.uk/subjects/chemistry/gcse/chemistry-8462/specification/subject-content/chemical-analysis"
CATALOGUE_VERSION = "aqa-8462-ion-tests-v1"

# Each signature maps an observed outcome to (ion formula, signed charge).
# Reagent conditions are part of the test identifier.
SIGNATURES = {
    "flame": {
        "crimson": (("Li", 1),),
        "yellow": (("Na", 1),),
        "lilac": (("K", 1),),
        "orange_red": (("Ca", 2),),
        "green": (("Cu", 2),),
    },
    "sodium_hydroxide": {
        "white_precipitate": (("Al", 3), ("Ca", 2), ("Mg", 2)),
        "blue_precipitate": (("Cu", 2),),
        "green_precipitate": (("Fe", 2),),
        "brown_precipitate": (("Fe", 3),),
    },
    "excess_sodium_hydroxide": {
        "white_precipitate_dissolves": (("Al", 3),),
        "white_precipitate_remains": (("Ca", 2), ("Mg", 2)),
    },
    "silver_nitrate_nitric_acid": {
        "white_precipitate": (("Cl", -1),),
        "cream_precipitate": (("Br", -1),),
        "yellow_precipitate": (("I", -1),),
    },
    "barium_chloride_hydrochloric_acid": {
        "white_precipitate": (("SO4", -2),),
    },
    "acid_gas_limewater": {
        "limewater_turns_milky": (("CO3", -2),),
    },
}
