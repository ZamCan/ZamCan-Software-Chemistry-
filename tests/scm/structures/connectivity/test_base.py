import pytest

from scm.matter.atoms import Atom
from scm.structures.bonds import Bond, BondOrder
from scm.structures.connectivity import Connectivity


def test_empty_connectivity():
    graph = Connectivity()

    assert graph.nodes == ()
    assert graph.bonds == ()
    assert graph.component_count == 0
    assert not graph.is_connected


def test_single_node():
    h = Atom.create(1)

    graph = Connectivity(nodes=(h,))

    assert graph.contains(h)
    assert graph.degree(h) == 0
    assert graph.component_count == 1
    assert graph.is_connected


def test_water_like_connectivity():
    o = Atom.create(8)
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    oh1 = Bond(o, h1)
    oh2 = Bond(o, h2)

    graph = Connectivity(
        nodes=(o, h1, h2),
        bonds=(oh1, oh2),
    )

    assert graph.degree(o) == 2
    assert graph.degree(h1) == 1
    assert graph.degree(h2) == 1

    assert graph.neighbors(o) == (h1, h2)
    assert graph.bonds_for(o) == (oh1, oh2)

    assert graph.component_count == 1
    assert graph.is_connected


def test_identical_atoms_are_distinct_nodes():
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    assert h1 == h2
    assert h1 is not h2

    graph = Connectivity(nodes=(h1, h2))

    assert graph.contains(h1)
    assert graph.contains(h2)
    assert graph.component_count == 2


def test_disconnected_components():
    h1 = Atom.create(1)
    h2 = Atom.create(1)
    o = Atom.create(8)

    graph = Connectivity(
        nodes=(h1, h2, o),
        bonds=(Bond(h1, h2),),
    )

    assert graph.component_count == 2
    assert not graph.is_connected

    components = graph.connected_components()

    assert len(components) == 2
    assert components[0] == (h1, h2)
    assert components[1] == (o,)


def test_add_node_is_immutable():
    h = Atom.create(1)
    o = Atom.create(8)

    graph = Connectivity(nodes=(h,))
    expanded = graph.add_node(o)

    assert graph.nodes == (h,)
    assert expanded.nodes == (h, o)


def test_add_bond_is_immutable():
    h = Atom.create(1)
    o = Atom.create(8)

    bond = Bond(h, o, BondOrder.DOUBLE)

    graph = Connectivity(nodes=(h, o))
    connected = graph.add_bond(bond)

    assert graph.bonds == ()
    assert connected.bonds == (bond,)


def test_bond_endpoint_must_be_a_node():
    h = Atom.create(1)
    o = Atom.create(8)
    c = Atom.create(6)

    bond = Bond(h, o)

    with pytest.raises(ValueError):
        Connectivity(nodes=(h, c), bonds=(bond,))


def test_duplicate_bond_is_rejected():
    h = Atom.create(1)
    o = Atom.create(8)

    first = Bond(h, o)
    second = Bond(h, o)

    with pytest.raises(ValueError):
        Connectivity(
            nodes=(h, o),
            bonds=(first, second),
        )


def test_unknown_species_rejected():
    h = Atom.create(1)
    o = Atom.create(8)

    graph = Connectivity(nodes=(h,))

    with pytest.raises(ValueError):
        graph.neighbors(o)


def test_bond_count():
    o = Atom.create(8)
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    graph = Connectivity(
        nodes=(o, h1, h2),
        bonds=(Bond(o, h1), Bond(o, h2)),
    )

    assert len(graph.bonds) == 2
