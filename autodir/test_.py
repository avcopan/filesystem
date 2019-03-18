""" test the autodir module
"""
import os
import tempfile
import itertools
import numpy
import autodir
import autoinf
import automol

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__id_():
    """ test autodir.id_
    """
    rid = autodir.id_.identifier()
    assert autodir.id_.is_identifier(rid)
    assert not autodir.id_.is_identifier(rid + 'A')
    assert not autodir.id_.is_identifier(rid + ' ')

    test_path = os.path.join(TMP_DIR, 'id_test')
    os.mkdir(test_path)

    ref_rids = tuple(autodir.id_.identifier() for _ in range(10))
    dir_names = tuple(itertools.chain(ref_rids,
                                      map('A'.__add__, ref_rids),
                                      map(' '.__add__, ref_rids)))

    for dir_name in dir_names:
        dir_path = os.path.join(test_path, dir_name)
        os.mkdir(dir_path)

    rids = autodir.id_.directory_identifiers_at(test_path)
    assert set(rids) == set(ref_rids)


def test__species():
    """ test autodir.species
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2

    dir_path = autodir.species.directory_path(TMP_DIR, ich, mult)

    assert not os.path.isdir(dir_path)
    autodir.species.create(TMP_DIR, ich, mult)
    assert os.path.isdir(dir_path)

    inf_obj = autodir.species.read_information_file(TMP_DIR, ich, mult)
    assert inf_obj.inchi == ich
    assert inf_obj.smiles == r'[CH]=C/C=C\C=O'


def test__theory():
    """ test autodir.theory
    """
    method = 'rhf-mp2'
    basis = 'sto-3g'

    dir_path = autodir.theory.directory_path(TMP_DIR, method, basis)

    assert not os.path.isdir(dir_path)
    autodir.theory.create(TMP_DIR, method, basis)
    assert os.path.isdir(dir_path)


def test__run():
    """ test autodir.run
    """
    ref_scr_str = '<run script contents>'
    ref_inp_str = '<input file contents>'
    ref_out_str = '<output file contents'
    ref_function_val = 'val'
    ref_func_inf_obj = autoinf.Info(function_key=ref_function_val)
    ref_base_inf_obj = autodir.run.base_information(
        function='<function name>',
        function_info=ref_func_inf_obj,
        job='optimization',
        prog='psi4',
        method='rhf-mp2',
        basis='sto-3g',
        inchi='InChI=1S/H2O/h1H2',
        complete=False,
    )

    rid = autodir.id_.identifier()

    dir_path = autodir.run.directory_path(TMP_DIR, rid)

    assert not os.path.isdir(dir_path)
    autodir.run.create(TMP_DIR, rid)
    assert os.path.isdir(dir_path)

    # write information to the filesystem
    autodir.run.write_base_information_file(TMP_DIR, ref_base_inf_obj)
    autodir.run.write_run_script(TMP_DIR, ref_scr_str)
    autodir.run.write_input_file(TMP_DIR, rid, ref_inp_str)
    autodir.run.write_output_file(TMP_DIR, rid, ref_out_str)

    # read information from the filesystem
    base_inf_obj = autodir.run.read_base_information_file(TMP_DIR)
    scr_str = autodir.run.read_run_script(TMP_DIR)
    inp_str = autodir.run.read_input_file(TMP_DIR, rid)
    out_str = autodir.run.read_output_file(TMP_DIR, rid)

    assert base_inf_obj == ref_base_inf_obj
    assert scr_str == ref_scr_str
    assert inp_str == ref_inp_str
    assert out_str == ref_out_str

    # further test the information object
    assert not base_inf_obj.complete
    base_inf_obj.complete = True
    assert base_inf_obj.complete

    assert base_inf_obj.function_info == ref_func_inf_obj
    assert base_inf_obj.function_info.function_key == ref_function_val

    print(base_inf_obj)


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
    ref_inf_obj = autodir.lj.information(nsamp=ref_nsamp)

    dir_path = autodir.lj.directory_path(TMP_DIR, bath, pot)

    assert not os.path.isdir(dir_path)
    autodir.lj.create(TMP_DIR, bath, pot)
    assert os.path.isdir(dir_path)

    # write information to the filesystem
    autodir.lj.write_geometry_file(TMP_DIR, bath, pot, ref_geo)
    autodir.lj.write_bath_geometry_file(TMP_DIR, bath, pot, ref_bath_geo)
    autodir.lj.write_epsilon_file(TMP_DIR, bath, pot, ref_eps)
    autodir.lj.write_sigma_file(TMP_DIR, bath, pot, ref_sig)
    autodir.lj.write_information_file(TMP_DIR, bath, pot, ref_inf_obj)

    # read information from the filesystem
    geo = autodir.lj.read_geometry_file(TMP_DIR, bath, pot)
    bath_geo = autodir.lj.read_bath_geometry_file(TMP_DIR, bath, pot)
    eps = autodir.lj.read_epsilon_file(TMP_DIR, bath, pot)
    sig = autodir.lj.read_sigma_file(TMP_DIR, bath, pot)
    inf_obj = autodir.lj.read_information_file(TMP_DIR, bath, pot)

    assert automol.geom.almost_equal(geo, ref_geo)
    assert automol.geom.almost_equal(bath_geo, ref_bath_geo)
    assert numpy.isclose(eps, ref_eps)
    assert numpy.isclose(sig, ref_sig)
    assert inf_obj == ref_inf_obj
    assert inf_obj.nsamp == ref_nsamp

    inf_obj.nsamp = 45
    print(inf_obj)


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
    ref_base_inf_obj = autodir.conf.base_information(nsamp=ref_nsamp)

    rid = autodir.id_.identifier()

    dir_path = autodir.conf.directory_path(TMP_DIR, rid)

    assert not os.path.isdir(dir_path)
    autodir.conf.create(TMP_DIR, rid)
    assert os.path.isdir(dir_path)

    # write information to the filesystem
    autodir.conf.write_geometry_file(TMP_DIR, rid, ref_geo)
    autodir.conf.write_energy_file(TMP_DIR, rid, ref_ene)
    autodir.conf.write_base_information_file(TMP_DIR, ref_base_inf_obj)

    # read information from the filesystem
    geo = autodir.conf.read_geometry_file(TMP_DIR, rid)
    ene = autodir.conf.read_energy_file(TMP_DIR, rid)
    base_inf_obj = autodir.conf.read_base_information_file(TMP_DIR)

    assert numpy.isclose(ene, ref_ene)
    assert automol.geom.almost_equal(geo, ref_geo)
    assert base_inf_obj == ref_base_inf_obj
    assert base_inf_obj.nsamp == ref_nsamp

    print(autodir.conf.identifiers(TMP_DIR))

    base_inf_obj.nsamp = 10
    print(base_inf_obj)


if __name__ == '__main__':
    # test__theory()
    # test__id_()
    test__conf()
    test__lj()
    test__species()
    test__run()
