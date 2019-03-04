""" test the autodir module
"""
import os
import tempfile
import numpy
import autodir
import automol

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__species():
    """ test autodir.species
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2

    dir_path = autodir.species.directory_path(TMP_DIR, ich, mult)

    assert not os.path.isdir(dir_path)
    autodir.species.create(TMP_DIR, ich, mult)
    assert os.path.isdir(dir_path)

    inf = autodir.species.read_information_file(TMP_DIR, ich, mult)
    assert inf[autodir.species.INFO.ICH_KEY] == ich
    assert inf[autodir.species.INFO.SMI_KEY] == r'[CH]=C/C=C\C=O'


def test__theory():
    """ test autodir.theory
    """
    method = 'rhf-mp2'
    basis = 'sto-3g'

    dir_path = autodir.theory.directory_path(TMP_DIR, method, basis)

    assert not os.path.isdir(dir_path)
    autodir.theory.create(TMP_DIR, method, basis)
    assert os.path.isdir(dir_path)


def test__lj():
    """ test autodir.lj
    """
    bath = 'He'
    pot = 'LJ126'

    ref_geo = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
               ('N', (4.435924209, 0.16134481659, -0.05448080419)),
               ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    ref_bath_geo = (('He', (0., 0., 0.)),)
    ref_eps = 247.880866746988
    ref_sig = 3.55018590361446
    ref_nsamp = 40

    ref_inf = autodir.lj.INFO.ONEDMIN.dict(nsamp=ref_nsamp)
    dir_path = autodir.lj.directory_path(TMP_DIR, bath, pot)

    assert not os.path.isdir(dir_path)
    autodir.lj.create(TMP_DIR, bath, pot)
    assert os.path.isdir(dir_path)

    # write information to the filesystem
    autodir.lj.write_geometry_file(TMP_DIR, bath, pot, ref_geo)
    autodir.lj.write_bath_geometry_file(TMP_DIR, bath, pot, ref_bath_geo)
    autodir.lj.write_epsilon_file(TMP_DIR, bath, pot, ref_eps)
    autodir.lj.write_sigma_file(TMP_DIR, bath, pot, ref_sig)
    autodir.lj.write_information_file(TMP_DIR, bath, pot, ref_inf)

    # read information from the filesystem
    geo = autodir.lj.read_geometry_file(TMP_DIR, bath, pot)
    bath_geo = autodir.lj.read_bath_geometry_file(TMP_DIR, bath, pot)
    eps = autodir.lj.read_epsilon_file(TMP_DIR, bath, pot)
    sig = autodir.lj.read_sigma_file(TMP_DIR, bath, pot)
    inf = autodir.lj.read_information_file(TMP_DIR, bath, pot)

    assert automol.geom.almost_equal(geo, ref_geo)
    assert automol.geom.almost_equal(bath_geo, ref_bath_geo)
    assert numpy.isclose(eps, ref_eps)
    assert numpy.isclose(sig, ref_sig)
    assert inf == ref_inf
    assert inf[autodir.lj.INFO.ONEDMIN.NSAMP_KEY] == ref_nsamp


if __name__ == '__main__':
    test__lj()
    test__species()
    test__theory()
