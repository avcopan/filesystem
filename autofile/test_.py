""" test the autofile module
"""
import os
import tempfile
import numpy
import automol
import autofile

TMP_DIR = tempfile.mkdtemp()


def test__energy():
    """ test the energy read/write functions
    """
    ref_ene = -75.00613628303537
    file_prefix = os.path.join(TMP_DIR, 'h2o')
    file_name = autofile.name.energy(file_prefix)

    assert not os.path.isfile(file_name)
    autofile.write.energy(file_name, ref_ene)
    assert os.path.isfile(file_name)

    ene = autofile.read.energy(file_name)
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
    file_prefix = os.path.join(TMP_DIR, 'ch3oh')
    file_name = autofile.name.geometry(file_prefix)

    assert not os.path.isfile(file_name)
    autofile.write.geometry(file_name, ref_geo)
    assert os.path.isfile(file_name)

    geo = autofile.read.geometry(file_name)
    assert automol.geom.almost_equal(geo, ref_geo)


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

    file_prefix = os.path.join(TMP_DIR, 'ch3oh')
    file_name = autofile.name.zmatrix(file_prefix)

    assert not os.path.isfile(file_name)
    autofile.write.zmatrix(file_name, ref_zma)
    assert os.path.isfile(file_name)

    zma = autofile.read.zmatrix(file_name)

    assert automol.zmatrix.almost_equal(zma, ref_zma)


if __name__ == '__main__':
    test__energy()
    test__geometry()
    test__zmatrix()
