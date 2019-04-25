""" test autodir.lib
"""
import os
import tempfile
import numbers
import numpy
import automol
import autoinf
import autodir.lib

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__dir__species_trunk():
    """ test dir_.species_trunk
    """
    prefix = os.path.join(PREFIX, 'species_trunk')
    os.mkdir(prefix)

    spc_trunk_dsdir = autodir.lib.dir_.species_trunk()
    assert not spc_trunk_dsdir.exists(prefix)
    spc_trunk_dsdir.create(prefix)
    assert spc_trunk_dsdir.exists(prefix)


def test__dir__species_leaf():
    """ test dir_.species_leaf
    """
    prefix = os.path.join(PREFIX, 'species_leaf')
    os.mkdir(prefix)

    spc_trunk_dsdir = autodir.lib.dir_.species_trunk()
    spc_leaf_dsdir = autodir.lib.dir_.species_leaf(spc_trunk_dsdir)

    specs_lst = (
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 1),
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1-', 1),
        ('InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-', 2),
        ('InChI=1S/O', 1),
        ('InChI=1S/O', 3),
    )

    for specs in specs_lst:
        assert not spc_leaf_dsdir.exists(prefix, specs)
        spc_leaf_dsdir.create(prefix, specs)
        assert spc_leaf_dsdir.exists(prefix, specs)

    print(spc_leaf_dsdir.existing(prefix))
    assert spc_leaf_dsdir.existing(prefix) == tuple(sorted(specs_lst))


def test__dir__theory_leaf():
    """ test dir_.theory_leaf
    """
    prefix = os.path.join(PREFIX, 'theory_leaf')
    os.mkdir(prefix)

    spc_trunk_dsdir = autodir.lib.dir_.species_trunk()
    spc_leaf_dsdir = autodir.lib.dir_.species_leaf(spc_trunk_dsdir)
    thy_leaf_dsdir = autodir.lib.dir_.theory_leaf(spc_leaf_dsdir)

    spc_specs = ('InChI=1S/CH3/h1H3', 2)
    thy_specs_lst = (
        ('hf', 'sto-3g', True),
        ('hf', 'sto-3g', False),
        ('b3lyp', 'sto-3g', False),
        ('b3lyp', '6-31g*', False),
    )
    specs_lst = tuple(spc_specs + thy_specs for thy_specs in thy_specs_lst)

    for specs in specs_lst:
        assert not thy_leaf_dsdir.exists(prefix, specs)
        thy_leaf_dsdir.create(prefix, specs)
        assert thy_leaf_dsdir.exists(prefix, specs)

    print(spc_leaf_dsdir.existing(prefix))
    print(thy_leaf_dsdir.existing(prefix, spc_specs))
    assert spc_leaf_dsdir.existing(prefix) == (spc_specs,)
    assert (thy_leaf_dsdir.existing(prefix, spc_specs)
            == tuple(sorted(thy_specs_lst)))


def test__dir__conformer_trunk():
    """ test dir_.conformer_trunk
    """
    prefix = os.path.join(PREFIX, 'conformer_trunk')
    os.mkdir(prefix)

    spc_trunk_dsdir = autodir.lib.dir_.species_trunk()
    spc_leaf_dsdir = autodir.lib.dir_.species_leaf(spc_trunk_dsdir)
    thy_leaf_dsdir = autodir.lib.dir_.theory_leaf(spc_leaf_dsdir)
    cnf_trunk_dsdir = autodir.lib.dir_.conformer_trunk(thy_leaf_dsdir)

    spc_specs = ('InChI=1S/CH3/h1H3', 2)
    thy_specs_lst = (
        ('hf', 'sto-3g', True),
        ('hf', 'sto-3g', False),
        ('b3lyp', 'sto-3g', False),
        ('b3lyp', '6-31g*', False),
    )
    specs_lst = tuple(spc_specs + thy_specs for thy_specs in thy_specs_lst)

    for specs in specs_lst:
        assert not cnf_trunk_dsdir.exists(prefix, specs)
        cnf_trunk_dsdir.create(prefix, specs)
        assert cnf_trunk_dsdir.exists(prefix, specs)


def test__dir__conformer_leaf():
    """ test dir_.conformer_leaf
    """
    prefix = os.path.join(PREFIX, 'conformer_leaf')
    os.mkdir(prefix)

    spc_trunk_dsdir = autodir.lib.dir_.species_trunk()
    spc_leaf_dsdir = autodir.lib.dir_.species_leaf(spc_trunk_dsdir)
    thy_leaf_dsdir = autodir.lib.dir_.theory_leaf(spc_leaf_dsdir)
    cnf_trunk_dsdir = autodir.lib.dir_.conformer_trunk(thy_leaf_dsdir)
    cnf_leaf_dsdir = autodir.lib.dir_.conformer_leaf(cnf_trunk_dsdir)

    nconfs = 10
    spc_seg_specs = ('InChI=1S/CH3/h1H3', 2)
    thy_seg_specs = ('hf', 'sto-3g', False)
    cnf_seg_specs_lst = tuple((autodir.lib.generate_new_conformer_id(),)
                              for _ in range(nconfs))
    spc_specs = spc_seg_specs
    thy_specs = spc_specs + thy_seg_specs
    specs_lst = tuple(thy_specs + cnf_seg_specs
                      for cnf_seg_specs in cnf_seg_specs_lst)

    for specs in specs_lst:
        assert not cnf_leaf_dsdir.exists(prefix, specs)
        cnf_leaf_dsdir.create(prefix, specs)
        assert cnf_leaf_dsdir.exists(prefix, specs)

    print(spc_leaf_dsdir.existing(prefix))
    print(thy_leaf_dsdir.existing(prefix, spc_specs))
    print(cnf_leaf_dsdir.existing(prefix, thy_specs))
    assert spc_leaf_dsdir.existing(prefix) == (spc_seg_specs,)
    assert thy_leaf_dsdir.existing(prefix, spc_specs) == (thy_seg_specs,)
    assert (cnf_leaf_dsdir.existing(prefix, thy_specs)
            == tuple(sorted(cnf_seg_specs_lst)))


def test__file__input_file():
    """ test autodir.lib.file_.input_file
    """
    ref_inp_str = '<input file contents>'

    inp_dfile = autodir.lib.file_.input_file('test')

    assert not inp_dfile.exists(PREFIX)
    inp_dfile.write(ref_inp_str, PREFIX)
    assert inp_dfile.exists(PREFIX)

    inp_str = inp_dfile.read(PREFIX)
    assert inp_str == ref_inp_str
    print(inp_str)


def test__file__output_file():
    """ test autodir.lib.file_.output_file
    """
    ref_out_str = '<output file contents>'

    out_dfile = autodir.lib.file_.output_file('test')

    assert not out_dfile.exists(PREFIX)
    out_dfile.write(ref_out_str, PREFIX)
    assert out_dfile.exists(PREFIX)

    out_str = out_dfile.read(PREFIX)
    assert out_str == ref_out_str
    print(out_str)


def test__file__information():
    """ test autodir.lib.file_.information
    """
    def information(nsamp, tors_info):
        """ base information object
        """
        tors_info = autoinf.Info(**dict(tors_info))
        assert isinstance(nsamp, numbers.Integral)
        inf_obj = autoinf.Info(nsamp=nsamp, tors_info=tors_info)
        assert autoinf.matches_function_signature(inf_obj, information)
        return inf_obj

    ref_inf_obj = information(
        nsamp=4, tors_info={'d1': (0., 1.), 'd2': (0., 3.)})

    inf_dfile = autodir.lib.file_.information('test', function=information)

    assert not inf_dfile.exists(PREFIX)
    inf_dfile.write(ref_inf_obj, PREFIX)
    assert inf_dfile.exists(PREFIX)

    inf_obj = inf_dfile.read(PREFIX)
    assert inf_obj == ref_inf_obj
    print(inf_obj)


def test__file__energy():
    """ test autodir.lib.file_.energy
    """
    ref_ene = -187.38518070487598

    ene_dfile = autodir.lib.file_.energy('test')

    assert not ene_dfile.exists(PREFIX)
    ene_dfile.write(ref_ene, PREFIX)
    assert ene_dfile.exists(PREFIX)

    ene = ene_dfile.read(PREFIX)
    assert numpy.isclose(ene, ref_ene)
    print(ene)


def test__file__geometry():
    """ test autodir.lib.file_.geometry
    """
    ref_geo = (('C', (0.066541036329, -0.86543409422, -0.56994517889)),
               ('O', (0.066541036329, -0.86543409422, 2.13152981129)),
               ('O', (0.066541036329, 1.6165813318, -1.63686376233)),
               ('H', (-1.52331011945, -1.99731957213, -1.31521725797)),
               ('H', (1.84099386813, -1.76479255185, -1.16213243427)),
               ('H', (-1.61114836922, -0.17751142359, 2.6046492029)),
               ('H', (-1.61092727126, 2.32295906780, -1.19178601663)))

    geo_dfile = autodir.lib.file_.geometry('test')

    assert not geo_dfile.exists(PREFIX)
    geo_dfile.write(ref_geo, PREFIX)
    assert geo_dfile.exists(PREFIX)

    geo = geo_dfile.read(PREFIX)
    assert automol.geom.almost_equal(geo, ref_geo)
    print(geo)


def test__file__gradient():
    """ test autodir.lib.file_.gradient
    """
    ref_grad = ((0.00004103632, 0.00003409422, 0.00004517889),
                (0.00004103632, 0.00003409422, 0.00002981129),
                (0.00004103632, 0.00008133180, 0.00006376233),
                (0.00001011945, 0.00001957213, 0.00001725797),
                (0.00009386813, 0.00009255185, 0.00003243427),
                (0.00004836922, 0.00001142359, 0.00004920290),
                (0.00002727126, 0.00005906780, 0.00008601663))

    grad_dfile = autodir.lib.file_.gradient('test')

    assert not grad_dfile.exists(PREFIX)
    grad_dfile.write(ref_grad, PREFIX)
    assert grad_dfile.exists(PREFIX)

    grad = grad_dfile.read(PREFIX)
    assert numpy.allclose(grad, ref_grad)
    print(grad)


def test__file__hessian():
    """ test autodir.lib.file_.hessian
    """
    ref_hess = (
        (-0.21406, 0., 0., -0.06169, 0., 0., 0.27574, 0., 0.),
        (0., 2.05336, 0.12105, 0., -0.09598, 0.08316, 0., -1.95737, -0.20421),
        (0., 0.12105, 0.19177, 0., -0.05579, -0.38831, 0., -0.06525, 0.19654),
        (-0.06169, 0., 0., 0.0316, 0., 0., 0.03009, 0., 0.),
        (0., -0.09598, -0.05579, 0., 0.12501, -0.06487, 0., -0.02902,
         0.12066),
        (0., 0.08316, -0.38831, 0., -0.06487, 0.44623, 0., -0.01829,
         -0.05792),
        (0.27574, 0., 0., 0.03009, 0., 0., -0.30583, 0., 0.),
        (0., -1.95737, -0.06525, 0., -0.02902, -0.01829, 0., 1.9864,
         0.08354),
        (0., -0.20421, 0.19654, 0., 0.12066, -0.05792, 0., 0.08354,
         -0.13862))

    hess_dfile = autodir.lib.file_.hessian('test')

    assert not hess_dfile.exists(PREFIX)
    hess_dfile.write(ref_hess, PREFIX)
    assert hess_dfile.exists(PREFIX)

    hess = hess_dfile.read(PREFIX)
    assert numpy.allclose(hess, ref_hess)
    print(hess)


def test__file__zmatrix():
    """ test autodir.lib.file_.zmatrix
    """
    ref_zma = (
        (('C', (None, None, None), (None, None, None)),
         ('O', (0, None, None), ('r1', None, None)),
         ('O', (0, 1, None), ('r2', 'a1', None)),
         ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
         ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
         ('H', (1, 0, 2), ('r5', 'a4', 'd3')),
         ('H', (2, 0, 1), ('r6', 'a5', 'd4'))),
        {'r1': 2.65933,
         'r2': 2.65933, 'a1': 1.90743,
         'r3': 2.06844, 'a2': 1.93366, 'd1': 4.1477,
         'r4': 2.06548, 'a3': 1.89469, 'd2': 2.06369,
         'r5': 1.83126, 'a4': 1.86751, 'd3': 1.44253,
         'r6': 1.83126, 'a5': 1.86751, 'd4': 4.84065})

    zma_dfile = autodir.lib.file_.zmatrix('test')

    assert not zma_dfile.exists(PREFIX)
    zma_dfile.write(ref_zma, PREFIX)
    assert zma_dfile.exists(PREFIX)

    zma = zma_dfile.read(PREFIX)
    assert automol.zmatrix.almost_equal(zma, ref_zma)
    print(zma)


def test__file__vmatrix():
    """ test autodir.lib.file_.vmatrix
    """
    ref_vma = (('C', (None, None, None), (None, None, None)),
               ('O', (0, None, None), ('r1', None, None)),
               ('O', (0, 1, None), ('r2', 'a1', None)),
               ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
               ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
               ('H', (1, 0, 2), ('r5', 'a4', 'd3')),
               ('H', (2, 0, 1), ('r6', 'a5', 'd4')))

    vma_dfile = autodir.lib.file_.vmatrix('test')

    assert not vma_dfile.exists(PREFIX)
    vma_dfile.write(ref_vma, PREFIX)
    assert vma_dfile.exists(PREFIX)

    vma = vma_dfile.read(PREFIX)
    assert vma == ref_vma
    print(vma)


def test__file__trajectory():
    """ test autodir.lib.file_.trajectory
    """
    ref_geos = [
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
         ('H', (-1.36240560905, 3.348313125118, 0.1732746576216)))]
    ref_comments = ['energy: -187.3894105487809',
                    'energy: -187.3850624381528']

    ref_traj = list(zip(ref_comments, ref_geos))

    traj_dfile = autodir.lib.file_.trajectory('test')

    assert not traj_dfile.exists(PREFIX)
    traj_dfile.write(ref_traj, PREFIX)
    assert traj_dfile.exists(PREFIX)

    # I'm not going to bother implementing a reader, since the trajectory files
    # are for human use only -- we aren't going to use this for data storage


def test__file__lennard_jones_epsilon():
    """ test autodir.lib.file_.lennard_jones_epsilon
    """
    ref_eps = 247.880866746988

    eps_dfile = autodir.lib.file_.lennard_jones_epsilon('test')

    assert not eps_dfile.exists(PREFIX)
    eps_dfile.write(ref_eps, PREFIX)
    assert eps_dfile.exists(PREFIX)

    eps = eps_dfile.read(PREFIX)
    assert numpy.isclose(eps, ref_eps)
    print(eps)


def test__file__lennard_jones_sigma():
    """ test autodir.lib.file_.lennard_jones_sigma
    """
    ref_sig = 3.55018590361446

    sig_dfile = autodir.lib.file_.lennard_jones_sigma('test')

    assert not sig_dfile.exists(PREFIX)
    sig_dfile.write(ref_sig, PREFIX)
    assert sig_dfile.exists(PREFIX)

    sig = sig_dfile.read(PREFIX)
    assert numpy.isclose(sig, ref_sig)
    print(sig)


if __name__ == '__main__':
    test__dir__species_trunk()
    test__dir__species_leaf()
    test__dir__theory_leaf()
    test__dir__conformer_trunk()
    test__dir__conformer_leaf()
    test__file__input_file()
    test__file__output_file()
    test__file__information()
    test__file__energy()
    test__file__geometry()
    test__file__gradient()
    test__file__hessian()
    test__file__zmatrix()
    test__file__vmatrix()
    test__file__trajectory()
    test__file__lennard_jones_epsilon()
    test__file__lennard_jones_sigma()
