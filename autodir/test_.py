""" test the autodir module
"""
import os
import tempfile
import autodir

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__species():
    """ test species directory creation
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    schem = autodir.species.schema(ich, mult)
    autodir.schema.create(prefix=TMP_DIR, schem=schem)
    assert os.path.exists(os.path.join(TMP_DIR, schem[0]))

    dir_path, _ = schem
    print(dir_path)


def test__theory():
    """ test theory directory creation
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    schem1 = autodir.species.schema(ich, mult)
    dir_path1 = autodir.schema.create(prefix=TMP_DIR, schem=schem1)

    method = 'rhf-mp2'
    basis = 'sto-3g'
    schem2 = autodir.theory.schema(method, basis)
    dir_path2 = autodir.schema.create(prefix=dir_path1, schem=schem2)

    assert os.path.exists(dir_path2)

    print(dir_path2)


def test__lj():
    """ test lennard-jones directory creation
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    schem1 = autodir.species.schema(ich, mult)
    dir_path1 = autodir.schema.create(prefix=TMP_DIR, schem=schem1)

    method = 'rhf-mp2'
    basis = 'sto-3g'
    schem2 = autodir.theory.schema(method, basis)
    dir_path2 = autodir.schema.create(prefix=dir_path1, schem=schem2)

    bath_gas = 'He'
    method = 'LJ126'
    geo = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
           ('N', (4.435924209, 0.16134481659, -0.05448080419)),
           ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    bath_geo = (('He', (0., 0., 0.)),)
    eps = 247.880866746988
    sig = 3.55018590361446
    nsamp = 40

    schem3 = autodir.lj.schema(
        bath_gas, method, geo=geo, bath_geo=bath_geo,
        eps=eps, sig=sig, nsamp=nsamp)
    dir_path3 = autodir.schema.create(prefix=dir_path2, schem=schem3)
    print(dir_path3)


if __name__ == '__main__':
    # test__species()
    # test__theory()
    test__lj()
