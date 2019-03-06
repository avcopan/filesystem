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


def test__conf():
    """ test autodir.conf
    """
    ref_geo = (('C', (0.066541036329, -0.86543409422, -0.56994517889)),
               ('O', (0.066541036329, -0.86543409422, 2.13152981129)),
               ('O', (0.066541036329, 1.6165813318, -1.63686376233)),
               ('H', (-1.52331011945, -1.99731957213, -1.31521725797)),
               ('H', (1.84099386813, -1.76479255185, -1.16213243427)),
               ('H', (-1.61114836922, -0.17751142359, 2.6046492029)),
               ('H', (-1.61092727126, 2.32295906780, -1.19178601663)))
    ref_ene = -187.38518070487598
    ref_nsamp = 7
    ref_base_inf = autodir.conf.INFO.BASE.dict(nsamp=ref_nsamp)

    uid = autodir.unique_identifier()
    dir_path = autodir.conf.directory_path(TMP_DIR, uid)

    assert not os.path.isdir(dir_path)
    autodir.conf.create(TMP_DIR, uid)
    assert os.path.isdir(dir_path)

    # write information to the filesystem
    autodir.conf.write_geometry_file(TMP_DIR, uid, ref_geo)
    autodir.conf.write_energy_file(TMP_DIR, uid, ref_ene)
    autodir.conf.write_base_information_file(TMP_DIR, ref_base_inf)

    # read information from the filesystem
    geo = autodir.conf.read_geometry_file(TMP_DIR, uid)
    ene = autodir.conf.read_energy_file(TMP_DIR, uid)
    base_inf = autodir.conf.read_base_information_file(TMP_DIR)

    assert numpy.isclose(ene, ref_ene)
    assert automol.geom.almost_equal(geo, ref_geo)
    assert base_inf == ref_base_inf
    print(dir_path)

    print(autodir.conf.existing_identifiers(TMP_DIR))


if __name__ == '__main__':
    test__lj()
    test__species()
    test__theory()
    test__conf()
