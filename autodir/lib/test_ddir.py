""" test autodir.lib.ddir
"""
import tempfile
from autodir.lib import dname
from autodir.lib import ddir

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species_trunk():
    """ tets ddir.species_trunk
    """
    spc_trunk_ddir = ddir.species_trunk()
    assert not spc_trunk_ddir.exists(PREFIX)
    spc_trunk_ddir.create(PREFIX)
    assert spc_trunk_ddir.exists(PREFIX)


def test__species_leaf():
    """ tets ddir.species_leaf
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    args = [ich, mult]

    spc_leaf_ddir = ddir.species_leaf()
    assert not spc_leaf_ddir.exists(PREFIX, args)
    spc_leaf_ddir.create(PREFIX, args)
    assert spc_leaf_ddir.exists(PREFIX, args)


def test__theory_leaf():
    """ tets ddir.theory_leaf
    """
    method = 'b3lyp'
    basis = '6-31g*'
    orb_restricted = False
    args = [method, basis, orb_restricted]

    thr_leaf_ddir = ddir.theory_leaf()
    assert not thr_leaf_ddir.exists(PREFIX, args)
    thr_leaf_ddir.create(PREFIX, args)
    assert thr_leaf_ddir.exists(PREFIX, args)


def test__conformer_trunk():
    """ tets ddir.conformer_trunk
    """
    spc_trunk_ddir = ddir.conformer_trunk()
    assert not spc_trunk_ddir.exists(PREFIX)
    spc_trunk_ddir.create(PREFIX)
    assert spc_trunk_ddir.exists(PREFIX)


def test__conformer_leaf():
    """ tets ddir.conformer_leaf
    """
    cid = dname.new_conformer_id()
    args = [cid]
    print(cid)

    spc_leaf_ddir = ddir.conformer_leaf()
    assert not spc_leaf_ddir.exists(PREFIX, args)
    spc_leaf_ddir.create(PREFIX, args)
    assert spc_leaf_ddir.exists(PREFIX, args)


if __name__ == '__main__':
    test__species_trunk()
    test__species_leaf()
    test__theory_leaf()
    test__conformer_trunk()
    test__conformer_leaf()
