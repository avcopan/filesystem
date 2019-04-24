""" test autodir.lib.ddir
"""
import tempfile
import autodir.lib
from autodir.lib import dir_

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species_trunk():
    """ tets dir_.species_trunk
    """
    spc_trunk_ddir = dir_.species_trunk()
    assert not spc_trunk_ddir.exists(PREFIX)
    spc_trunk_ddir.create(PREFIX)
    assert spc_trunk_ddir.exists(PREFIX)


def test__species_leaf():
    """ tets dir_.species_leaf
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    args = [ich, mult]

    spc_leaf_ddir = dir_.species_leaf()
    assert not spc_leaf_ddir.exists(PREFIX, args)
    spc_leaf_ddir.create(PREFIX, args)
    assert spc_leaf_ddir.exists(PREFIX, args)


def test__theory_leaf():
    """ tets dir_.theory_leaf
    """
    method = 'b3lyp'
    basis = '6-31g*'
    orb_restricted = False
    args = [method, basis, orb_restricted]

    thr_leaf_ddir = dir_.theory_leaf()
    assert not thr_leaf_ddir.exists(PREFIX, args)
    thr_leaf_ddir.create(PREFIX, args)
    assert thr_leaf_ddir.exists(PREFIX, args)


def test__conformer_trunk():
    """ tets dir_.conformer_trunk
    """
    spc_trunk_ddir = dir_.conformer_trunk()
    assert not spc_trunk_ddir.exists(PREFIX)
    spc_trunk_ddir.create(PREFIX)
    assert spc_trunk_ddir.exists(PREFIX)


def test__conformer_leaf():
    """ tets dir_.conformer_leaf
    """
    cid = autodir.lib.name.new_conformer_id()
    args = [cid]

    spc_leaf_ddir = dir_.conformer_leaf()
    assert not spc_leaf_ddir.exists(PREFIX, args)
    spc_leaf_ddir.create(PREFIX, args)
    assert spc_leaf_ddir.exists(PREFIX, args)


if __name__ == '__main__':
    # test__species_trunk()
    test__species_leaf()
    # test__theory_leaf()
    # test__conformer_trunk()
    # test__conformer_leaf()
    # test__species_leaf()
