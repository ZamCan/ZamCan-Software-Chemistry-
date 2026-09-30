import pytest

from scm.matter.atoms import Atom
from scm.matter.ions import Ion
from scm.structures.bonds import Bond, BondOrder, BondType


def test_single_covalent_bond():
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    bond = Bond(h1, h2)

    assert bond.first == h1
    assert bond.second == h2
    assert bond.order is BondOrder.SINGLE
    assert bond.bond_type is BondType.COVALENT
    assert bond.order_value == 1.0


def test_double_bond():
    c = Atom.create(6)
    o = Atom.create(8)

    bond = Bond(c, o, BondOrder.DOUBLE)

    assert bond.order is BondOrder.DOUBLE
    assert bond.order_value == 2.0


def test_string_values_are_normalized():
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    bond = Bond(h1, h2, "single", "covalent")

    assert bond.order is BondOrder.SINGLE
    assert bond.bond_type is BondType.COVALENT


def test_bond_endpoints():
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    bond = Bond(h1, h2)

    assert bond.endpoints == (h1, h2)
    assert bond.connects(h1)
    assert bond.connects(h2)
    assert bond.other(h1) == h2
    assert bond.other(h2) == h1


def test_other_rejects_non_endpoint():
    h1 = Atom.create(1)
    h2 = Atom.create(1)
    o = Atom.create(8)

    bond = Bond(h1, h2)

    with pytest.raises(ValueError):
        bond.other(o)


def test_self_bond_is_rejected():
    h = Atom.create(1)

    with pytest.raises(ValueError):
        Bond(h, h)


def test_reversed_bond():
    h = Atom.create(1)
    o = Atom.create(8)

    bond = Bond(h, o, BondOrder.DOUBLE)
    reversed_bond = bond.reversed()

    assert reversed_bond.first == o
    assert reversed_bond.second == h
    assert reversed_bond.order is BondOrder.DOUBLE


def test_non_species_endpoint_is_rejected():
    with pytest.raises(TypeError):
        Bond("H", "O")


def test_ionic_bond():
    na = Ion.create(11, 1)
    cl = Ion.create(17, -1)

    bond = Bond(na, cl, BondOrder.SINGLE, BondType.IONIC)

    assert bond.is_ionic
    assert not bond.is_covalent


def test_aromatic_order():
    c1 = Atom.create(6)
    c2 = Atom.create(6)

    bond = Bond(c1, c2, BondOrder.AROMATIC)

    assert bond.is_aromatic
    assert bond.order_value == 1.5
