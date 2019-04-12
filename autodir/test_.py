""" test the autodir module
"""
import os
import time
import tempfile
import itertools
import numpy
import autodir
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
    method = 'b3lyp'
    basis = 'sto-3g'
    open_shell = True
    orb_restricted = False

    dir_path = autodir.theory.directory_path(
        TMP_DIR, method, basis, open_shell, orb_restricted)

    assert not os.path.isdir(dir_path)
    autodir.theory.create(
        TMP_DIR, method, basis, open_shell, orb_restricted)
    assert os.path.isdir(dir_path)

    autodir.theory.create(
        TMP_DIR, method, basis, False, True)

    autodir.theory.create(
        TMP_DIR, method, '6-31g*', False, True)


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


def test__run():
    """ test autodir.run
    """
    ref_inf_obj = autodir.run.information(
        job='optimization',
        prog='psi4',
        method='mp2',
        basis='sto-3g',
    )
    ref_inp_str = '<input file contents>'
    ref_out_str = '<output file contents>'

    name = autodir.par.DirectoryName.Run.OPT

    dir_path = autodir.run.directory_path(TMP_DIR, name)
    assert not os.path.isdir(dir_path)
    autodir.run.create(TMP_DIR, name)
    assert os.path.isdir(dir_path)

    autodir.run.add_start_time_to_information(ref_inf_obj)
    time.sleep(1)
    autodir.run.add_end_time_to_information(ref_inf_obj)

    # write information to the filesystem
    autodir.run.write_information_file(TMP_DIR, name, ref_inf_obj)
    autodir.run.write_input_file(TMP_DIR, name, ref_inp_str)
    autodir.run.write_output_file(TMP_DIR, name, ref_out_str)

    # read information from the filesystem
    inf_obj = autodir.run.read_information_file(TMP_DIR, name)
    inp_str = autodir.run.read_input_file(TMP_DIR, name)
    out_str = autodir.run.read_output_file(TMP_DIR, name)

    assert inf_obj == ref_inf_obj
    assert inp_str == ref_inp_str
    assert out_str == ref_out_str

    time_elapsed = inf_obj.utc_end_time - inf_obj.utc_start_time
    assert time_elapsed.days == 0 and time_elapsed.seconds == 1


def test__conf():
    """ test autodir.conf
    """
    # # base
    ref_nsamp = 7
    tors_info = {'d3': (0, 6.283185307179586),
                 'd4': (0, 6.283185307179586)}
    ref_base_inf_obj = autodir.conf.base_information(
        nsamp=ref_nsamp, tors_info=tors_info)
    ref_base_vma = (('C', (None, None, None), (None, None, None)),
                    ('O', (0, None, None), ('r1', None, None)),
                    ('O', (0, 1, None), ('r2', 'a1', None)),
                    ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
                    ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
                    ('H', (1, 0, 2), ('r5', 'a4', 'd3')),
                    ('H', (2, 0, 1), ('r6', 'a5', 'd4')))

    # # geometry
    ref_inf_obj = autodir.run.information(
        job='optimization', prog='psi4', method='mp2', basis='sto-3g')
    ref_inp_str = '<geometry input file>'
    ref_geo = (('C', (0.066541036329, -0.86543409422, -0.56994517889)),
               ('O', (0.066541036329, -0.86543409422, 2.13152981129)),
               ('O', (0.066541036329, 1.6165813318, -1.63686376233)),
               ('H', (-1.52331011945, -1.99731957213, -1.31521725797)),
               ('H', (1.84099386813, -1.76479255185, -1.16213243427)),
               ('H', (-1.61114836922, -0.17751142359, 2.6046492029)),
               ('H', (-1.61092727126, 2.32295906780, -1.19178601663)))
    ref_ene = -187.38518070487598

    # # gradient
    ref_grad_inf_obj = autodir.run.information(
        job='gradient', prog='psi4', method='mp2', basis='sto-3g')
    ref_grad_inp_str = '<grad input file>'
    ref_grad = ((0.00004103632, 0.00003409422, 0.00004517889),
                (0.00004103632, 0.00003409422, 0.00002981129),
                (0.00004103632, 0.00008133180, 0.00006376233),
                (0.00001011945, 0.00001957213, 0.00001725797),
                (0.00009386813, 0.00009255185, 0.00003243427),
                (0.00004836922, 0.00001142359, 0.00004920290),
                (0.00002727126, 0.00005906780, 0.00008601663))

    rid = autodir.id_.identifier()

    dir_path = autodir.conf.directory_path(TMP_DIR, rid)

    assert not os.path.isdir(dir_path)
    autodir.conf.create(TMP_DIR, rid)
    assert os.path.isdir(dir_path)

    run_dir_path = autodir.conf.run_directory_path(TMP_DIR, rid)
    assert not os.path.isdir(run_dir_path)
    autodir.conf.create_run_directory(TMP_DIR, rid)
    assert os.path.isdir(run_dir_path)

    # write information to the filesystem
    # # base
    autodir.conf.write_base_information_file(TMP_DIR, ref_base_inf_obj)
    autodir.conf.write_base_vmatrix_file(TMP_DIR, ref_base_vma)

    # # geometry
    autodir.conf.write_information_file(TMP_DIR, rid, ref_inf_obj)
    autodir.conf.write_input_file(TMP_DIR, rid, ref_inp_str)
    autodir.conf.write_geometry_file(TMP_DIR, rid, ref_geo)
    autodir.conf.write_energy_file(TMP_DIR, rid, ref_ene)

    # # gradient
    autodir.conf.write_gradient_information_file(
        TMP_DIR, rid, ref_grad_inf_obj)
    autodir.conf.write_gradient_input_file(TMP_DIR, rid, ref_grad_inp_str)
    autodir.conf.write_gradient_file(TMP_DIR, rid, ref_grad)

    # read information from the filesystem
    # # base
    base_inf_obj = autodir.conf.read_base_information_file(TMP_DIR)
    base_vma = autodir.conf.read_base_vmatrix_file(TMP_DIR)
    assert base_inf_obj == ref_base_inf_obj
    assert base_inf_obj.nsamp == ref_nsamp
    assert base_vma == ref_base_vma

    # # geometry
    inf_obj = autodir.conf.read_information_file(TMP_DIR, rid)
    inp_str = autodir.conf.read_input_file(TMP_DIR, rid)
    geo = autodir.conf.read_geometry_file(TMP_DIR, rid)
    ene = autodir.conf.read_energy_file(TMP_DIR, rid)
    assert inf_obj == ref_inf_obj
    assert inp_str == ref_inp_str
    assert numpy.isclose(ene, ref_ene)
    assert automol.geom.almost_equal(geo, ref_geo)

    # # gradient
    grad_inf_obj = autodir.conf.read_gradient_information_file(TMP_DIR, rid)
    grad_inp_str = autodir.conf.read_gradient_input_file(TMP_DIR, rid)
    grad = autodir.conf.read_gradient_file(TMP_DIR, rid)
    assert grad_inf_obj == ref_grad_inf_obj
    assert grad_inp_str == ref_grad_inp_str
    assert numpy.allclose(grad, ref_grad)

    base_inf_obj.nsamp = 10


def test__conf_trajectory():
    """ test the conformer trajectory update
    """
    rids = [autodir.id_.identifier() for _ in range(2)]
    geos = [
        (('C', (0.0, 0.0, 0.0)),
         ('O', (0.0, 0.0, 2.699694868173)),
         ('O', (0.0, 2.503038629201, -1.011409768236)),
         ('H', (-1.683942509299, -1.076047850358, -0.583313101501)),
         ('H', (1.684063451772, -0.943916309940, -0.779079279468)),
         ('H', (1.56980872050, 0.913848877557, 3.152002706027)),
         ('H', (-1.57051358834, 3.264399836517, -0.334901043405))),
        (('C', (0.0, 0.0, 0.0)),
         ('O', (0.0, 0.0, 2.70915105770)),
         ('O', (0.0, 2.55808068205, -0.83913477573)),
         ('H', (-1.660164085463, -1.04177010816, -0.73213470306)),
         ('H', (1.711679909369, -0.895873802652, -0.779058492481)),
         ('H', (0.0238181080852, -1.813377410537, 3.16912929390)),
         ('H', (-1.36240560905, 3.348313125118, 0.1732746576216))),
    ]
    enes = [
        -187.38941054878092,
        -187.3850624381528,
    ]

    for rid, geo, ene in zip(rids, geos, enes):
        autodir.conf.create(TMP_DIR, rid)
        autodir.conf.write_geometry_file(TMP_DIR, rid, geo)
        autodir.conf.write_energy_file(TMP_DIR, rid, ene)

    autodir.conf.update_trajectory_file(TMP_DIR)


def test__scan():
    """ test autodir.scan
    """
    ref_base_vma = (('C', (None, None, None), (None, None, None)),
                    ('O', (0, None, None), ('r1', None, None)),
                    ('O', (0, 1, None), ('r2', 'a1', None)),
                    ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
                    ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
                    ('H', (1, 0, 2), ('r5', 'a4', 'd3')),
                    ('H', (2, 0, 1), ('r6', 'a5', 'd4')))
    # tors_info = {'d3': (0, 6.283185307179586),
    #              'd4': (0, 6.283185307179586)}
    tors_dct = {'d3': 3, 'd4': 5}
    idxs_lst = list(itertools.product(range(3), range(5)))

    # # geometry
    ref_inf_obj = autodir.run.information(
        job='optimization', prog='psi4', method='mp2', basis='sto-3g')
    ref_inp_str = '<geometry input file>'
    ref_geo = (('C', (0.066541036329, -0.86543409422, -0.56994517889)),
               ('O', (0.066541036329, -0.86543409422, 2.13152981129)),
               ('O', (0.066541036329, 1.6165813318, -1.63686376233)),
               ('H', (-1.52331011945, -1.99731957213, -1.31521725797)),
               ('H', (1.84099386813, -1.76479255185, -1.16213243427)),
               ('H', (-1.61114836922, -0.17751142359, 2.6046492029)),
               ('H', (-1.61092727126, 2.32295906780, -1.19178601663)))
    ref_ene = -187.38518070487598

    # write information to the filesystem
    # # base
    autodir.scan.create_base(TMP_DIR)
    autodir.scan.write_base_vmatrix_file(TMP_DIR, ref_base_vma)

    # # geometry
    for idxs in idxs_lst:
        dir_path = autodir.scan.directory_path(TMP_DIR, tors_dct, idxs)
        assert not os.path.isdir(dir_path)
        autodir.scan.create(TMP_DIR, tors_dct, idxs)
        assert os.path.isdir(dir_path)

        autodir.scan.write_information_file(
            TMP_DIR, tors_dct, idxs, ref_inf_obj)
        autodir.scan.write_input_file(TMP_DIR, tors_dct, idxs, ref_inp_str)
        autodir.scan.write_geometry_file(TMP_DIR, tors_dct, idxs, ref_geo)
        autodir.scan.write_energy_file(TMP_DIR, tors_dct, idxs, ref_ene)

        # # geometry
        inf_obj = autodir.scan.read_information_file(TMP_DIR, tors_dct, idxs)
        inp_str = autodir.scan.read_input_file(TMP_DIR, tors_dct, idxs)
        geo = autodir.scan.read_geometry_file(TMP_DIR, tors_dct, idxs)
        ene = autodir.scan.read_energy_file(TMP_DIR, tors_dct, idxs)
        assert inf_obj == ref_inf_obj
        assert inp_str == ref_inp_str
        assert numpy.isclose(ene, ref_ene)
        assert automol.geom.almost_equal(geo, ref_geo)


if __name__ == '__main__':
    # test__species()
    # test__theory()
    # test__run()
    # test__conf_trajectory()
    # test__conf()
    test__scan()
