""" test the autofile module
"""
import os
import tempfile
import numpy
import automol
import autofile

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__information():
    """ test the information read/write functions
    """
    ref_inf = {'x': {'y': 1, 'z': 2}, 'a': ['b', 'c', 'd', 'e']}

    inf_file_name = autofile.name.information('test')
    inf_file_path = os.path.join(TMP_DIR, inf_file_name)
    inf_str = autofile.write.information(ref_inf)

    assert not os.path.isfile(inf_file_path)
    autofile.write_file(inf_file_path, inf_str)
    assert os.path.isfile(inf_file_path)

    inf_str = autofile.read_file(inf_file_path)
    inf = autofile.read.information(inf_str)
    assert inf == ref_inf


def test__energy():
    """ test the energy read/write functions
    """
    ref_ene = -75.00613628303537

    ene_file_name = autofile.name.energy('test')
    ene_file_path = os.path.join(TMP_DIR, ene_file_name)
    ene_str = autofile.write.energy(ref_ene)

    assert not os.path.isfile(ene_file_path)
    autofile.write_file(ene_file_path, ene_str)
    assert os.path.isfile(ene_file_path)

    ene_str = autofile.read_file(ene_file_path)
    ene = autofile.read.energy(ene_str)
    assert numpy.isclose(ref_ene, ene)


def test__geometry():
    """ test the geometry read/write functions
    """
    ref_geo = (('C', (-0.70116587131, 0.0146227007587, -0.016166607003)),
               ('O', (1.7323365056, -0.9538524899, -0.5617192010)),
               ('H', (-0.9827048283, 0.061897979239, 2.02901783816)),
               ('H', (-0.8787925682, 1.91673409124, -0.80019507919)),
               ('H', (-2.12093033745, -1.21447973767, -0.87411360631)),
               ('H', (2.9512589894, 0.17507745634, 0.22317665541)))

    geo_file_name = autofile.name.geometry('test')
    geo_file_path = os.path.join(TMP_DIR, geo_file_name)
    geo_str = autofile.write.geometry(ref_geo)

    assert not os.path.isfile(geo_file_path)
    autofile.write_file(geo_file_path, geo_str)
    assert os.path.isfile(geo_file_path)

    geo_str = autofile.read_file(geo_file_path)
    geo = autofile.read.geometry(geo_str)
    assert automol.geom.almost_equal(ref_geo, geo)


def test__zmatrix():
    """ test the zmatrix read/write functions
    """
    ref_zma = (
        (('C', (None, None, None), (None, None, None)),
         ('O', (0, None, None), ('R1', None, None)),
         ('H', (0, 1, None), ('R2', 'A2', None)),
         ('H', (0, 1, 2), ('R3', 'A3', 'D3')),
         ('H', (0, 1, 2), ('R4', 'A4', 'D4')),
         ('H', (1, 0, 2), ('R5', 'A5', 'D5'))),
        {'R1': 2.67535, 'R2': 2.06501, 'A2': 1.9116242,
         'R3': 2.06501, 'A3': 1.9116242, 'D3': 2.108497362,
         'R4': 2.06458, 'A4': 1.9020947, 'D4': 4.195841334,
         'R5': 1.83748, 'A5': 1.8690905, 'D5': 5.228936625})

    zma_file_name = autofile.name.zmatrix('test')
    zma_file_path = os.path.join(TMP_DIR, zma_file_name)
    zma_str = autofile.write.zmatrix(ref_zma)

    assert not os.path.isfile(zma_file_path)
    autofile.write_file(zma_file_path, zma_str)
    assert os.path.isfile(zma_file_path)

    zma_str = autofile.read_file(zma_file_path)
    zma = autofile.read.zmatrix(zma_str)
    assert automol.zmatrix.almost_equal(ref_zma, zma)


def test__lennard_jones_epsilon():
    """ test the epsilon read/write functions
    """
    ref_eps = 247.880866746988

    eps_file_name = autofile.name.lennard_jones_epsilon('test')
    eps_file_path = os.path.join(TMP_DIR, eps_file_name)
    eps_str = autofile.write.lennard_jones_epsilon(ref_eps)

    assert not os.path.isfile(eps_file_path)
    autofile.write_file(eps_file_path, eps_str)
    assert os.path.isfile(eps_file_path)

    eps_str = autofile.read_file(eps_file_path)
    eps = autofile.read.lennard_jones_epsilon(eps_str)
    assert numpy.isclose(ref_eps, eps)


def test__lennard_jones_sigma():
    """ test the sigma read/write functions
    """
    ref_sig = 3.55018590361446

    sig_file_name = autofile.name.lennard_jones_sigma('test')
    sig_file_path = os.path.join(TMP_DIR, sig_file_name)
    sig_str = autofile.write.lennard_jones_sigma(ref_sig)

    assert not os.path.isfile(sig_file_path)
    autofile.write_file(sig_file_path, sig_str)
    assert os.path.isfile(sig_file_path)

    sig_str = autofile.read_file(sig_file_path)
    sig = autofile.read.lennard_jones_sigma(sig_str)
    assert numpy.isclose(ref_sig, sig)


if __name__ == '__main__':
    test__information()
    test__energy()
    test__geometry()
    test__zmatrix()
    test__lennard_jones_epsilon()
    test__lennard_jones_sigma()
