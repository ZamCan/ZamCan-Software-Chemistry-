from scm.matter.atoms import neutral_atom
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies
from scm.matter.ions import Ion


def test_atom_is_chemical_species():
    atom = neutral_atom(
        11,
        symbol="Na",
    )

    assert atom.formula == "Na"
    assert atom.element_counts == {"Na": 1}
    assert atom.charge_number == 0
    assert atom.is_neutral


def test_ion_is_chemical_species():
    ion = Ion(
        atomic_number=11,
        charge_number=1,
        symbol="Na",
    )

    assert ion.formula == "Na"
    assert ion.element_counts == {"Na": 1}
    assert ion.charge_number == 1
    assert ion.electron_count == 10
    assert ion.is_cation


def test_chloride_is_chemical_species():
    ion = Ion(
        atomic_number=17,
        charge_number=-1,
        symbol="Cl",
    )

    assert ion.formula == "Cl"
    assert ion.element_counts == {"Cl": 1}
    assert ion.charge_number == -1
    assert ion.electron_count == 18
    assert ion.is_anion



def test_species_identity_key_is_deterministic():
    from scm.chemistry.identity_key import ChemicalIdentityKey

    first = ChemicalSpecies(
        Composition.from_mapping({"H": 2, "O": 1})
    )
    second = ChemicalSpecies(
        Composition.from_mapping({"O": 1, "H": 2})
    )

    assert first.identity_key == second.identity_key
    assert isinstance(first.identity_key, ChemicalIdentityKey)


def test_species_identity_key_includes_charge_and_radical():
    neutral = ChemicalSpecies(Composition.from_mapping({"O": 1}))
    ion = ChemicalSpecies(Composition.from_mapping({"O": 1}), charge_number=-1)
    radical = ChemicalSpecies(Composition.from_mapping({"O": 1}), radical=True)

    assert neutral.identity_key != ion.identity_key
    assert neutral.identity_key != radical.identity_key
