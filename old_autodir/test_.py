""" test autodir.lib.dlayer
"""
import os
import tempfile
import numpy
import automol
import autodir

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species():
    """ tets fsys.species
    """
    prefix = os.path.join(PREFIX, 'species')
    os.mkdir(prefix)

    args_lst = [
        ('InChI=1S/O', 3),
        ('InChI=1S/O', 1),
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 1),
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1-', 1),
        ('InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-', 2),
    ]

    # fs_ = autodir.filesystem()

    # for args in args_lst:
    #     assert not fs_.species.dir.exists(prefix, args)
    #     assert not fs_.species.file.info.exists(prefix, args)
    #     fs_.species.dir.create(prefix, args)
    #     assert fs_.species.dir.exists(prefix, args)
    #     assert fs_.species.file.info.exists(prefix, args)

    # assert fs_.species.dir.created_names(prefix) == (
    #     'SPC/C2H2F2/WFLOTYSKFUPZQB/1/OWOJBTED',
    #     'SPC/C2H2F2/WFLOTYSKFUPZQB/1/UPHRSURJ',
    #     'SPC/C5H5O/ZMKDIXNSHZUDML/2/ARJAWSKD',
    #     'SPC/O/QVGXLLKOCUKJST/1/UHFFFAOY',
    #     'SPC/O/QVGXLLKOCUKJST/3/UHFFFAOY'
    # )


def test__theory():
    """ tets fsys.theory
    """
    prefix = os.path.join(PREFIX, 'theory')
    os.mkdir(prefix)

    spc_args = ('InChI=1S/CH3/h1H3', 2)
    args_lst = [
        spc_args + ('hf', 'sto-3g', True),
        spc_args + ('hf', 'sto-3g', False),
        spc_args + ('b3lyp', 'sto-3g', False),
        spc_args + ('b3lyp', '6-31g*', False),
    ]

    # fs_ = autodir.filesystem()

    # for args in args_lst:
    #     assert not fs_.theory.dir.exists(prefix, args)
    #     assert not fs_.theory.file.info.exists(prefix, args)
    #     fs_.theory.dir.create(prefix, args)
    #     assert fs_.theory.dir.exists(prefix, args)
    #     assert fs_.theory.file.info.exists(prefix, args)

    # print(fs_.theory.dir.created_names(prefix))
    # # assert fs_.theory.dir.created_names(prefix, spc_args) == (
    # #     '_0gh69R', '_0gh69U', 'ezvh69R', 'ezvh69U', 'ezvlpJR', 'ezvlpJU')


def test__conformer():
    """ tets fsys.conformer
    """
    prefix = os.path.join(PREFIX, 'conformer')
    os.mkdir(prefix)

    nconfs = 10
    cids = (autodir.lib.name.new_conformer_id() for _ in range(nconfs))
    args_lst = [(cid,) for cid in cids]

    fs_ = fsys.conformer()
    assert not fs_.conformer_trunk.dir.exists(prefix)
    fs_.conformer_trunk.dir.create(prefix)
    assert fs_.conformer_trunk.dir.exists(prefix)

    # create the trunk information file
    ref_trunk_inf_obj = autodir.lib.info.conformer_trunk(
        nsamp=7, tors_info={'d3': (0, 6.283185307179586),
                            'd4': (0, 6.283185307179586)})
    fs_.conformer_trunk.file.info.write(ref_trunk_inf_obj, prefix)
    trunk_inf_obj = fs_.conformer_trunk.file.info.read(prefix)
    assert trunk_inf_obj == ref_trunk_inf_obj

    # create the trunk vmatrix file
    ref_trunk_vma = (('C', (None, None, None), (None, None, None)),
                     ('O', (0, None, None), ('r1', None, None)),
                     ('O', (0, 1, None), ('r2', 'a1', None)),
                     ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
                     ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
                     ('H', (1, 0, 2), ('r5', 'a4', 'd3')),
                     ('H', (2, 0, 1), ('r6', 'a5', 'd4')))
    fs_.conformer_trunk.file.vmatrix.write(ref_trunk_vma, prefix)
    trunk_vma = fs_.conformer_trunk.file.vmatrix.read(prefix)
    assert trunk_vma == ref_trunk_vma

    for args in args_lst:
        fs_.conformer.dir.create(prefix, args)

        ref_geom_inf_obj = autodir.lib.info.run(
            job='optimization', prog='psi4', method='mp2', basis='sto-3g')
        ref_grad_inf_obj = autodir.lib.info.run(
            job='gradient', prog='psi4', method='mp2', basis='sto-3g')
        ref_hess_inf_obj = autodir.lib.info.run(
            job='hessian', prog='psi4', method='mp2', basis='sto-3g')
        ref_geom_inp_str = '<geometry input file>'
        ref_grad_inp_str = '<gradient input file>'
        ref_hess_inp_str = '<hessian input file>'
        ref_ene = -187.38518070487598
        ref_geo = (('C', (0.066541036329, -0.86543409422, -0.56994517889)),
                   ('O', (0.066541036329, -0.86543409422, 2.13152981129)),
                   ('O', (0.066541036329, 1.6165813318, -1.63686376233)),
                   ('H', (-1.52331011945, -1.99731957213, -1.31521725797)),
                   ('H', (1.84099386813, -1.76479255185, -1.16213243427)),
                   ('H', (-1.61114836922, -0.17751142359, 2.6046492029)),
                   ('H', (-1.61092727126, 2.32295906780, -1.19178601663)))
        ref_grad = ((0.00004103632, 0.00003409422, 0.00004517889),
                    (0.00004103632, 0.00003409422, 0.00002981129),
                    (0.00004103632, 0.00008133180, 0.00006376233),
                    (0.00001011945, 0.00001957213, 0.00001725797),
                    (0.00009386813, 0.00009255185, 0.00003243427),
                    (0.00004836922, 0.00001142359, 0.00004920290),
                    (0.00002727126, 0.00005906780, 0.00008601663))
        # (I'm not bothering with the hessian for now)

        # writes
        fs_.conformer.file.geometry_information.write(
            ref_geom_inf_obj, prefix, args)
        fs_.conformer.file.gradient_information.write(
            ref_grad_inf_obj, prefix, args)
        fs_.conformer.file.hessian_information.write(
            ref_hess_inf_obj, prefix, args)
        fs_.conformer.file.geometry_input.write(ref_geom_inp_str, prefix, args)
        fs_.conformer.file.gradient_input.write(ref_grad_inp_str, prefix, args)
        fs_.conformer.file.hessian_input.write(ref_hess_inp_str, prefix, args)
        fs_.conformer.file.energy.write(ref_ene, prefix, args)
        fs_.conformer.file.geometry.write(ref_geo, prefix, args)
        fs_.conformer.file.gradient.write(ref_grad, prefix, args)

        # reads
        geom_inf_obj = fs_.conformer.file.geometry_information.read(prefix,
                                                                    args)
        grad_inf_obj = fs_.conformer.file.gradient_information.read(prefix,
                                                                    args)
        hess_inf_obj = fs_.conformer.file.hessian_information.read(prefix,
                                                                   args)
        geom_inp_str = fs_.conformer.file.geometry_input.read(prefix, args)
        grad_inp_str = fs_.conformer.file.gradient_input.read(prefix, args)
        hess_inp_str = fs_.conformer.file.hessian_input.read(prefix, args)
        ene = fs_.conformer.file.energy.read(prefix, args)
        geo = fs_.conformer.file.geometry.read(prefix, args)
        grad = fs_.conformer.file.gradient.read(prefix, args)

        # check read values
        assert geom_inf_obj == ref_geom_inf_obj
        assert grad_inf_obj == ref_grad_inf_obj
        assert hess_inf_obj == ref_hess_inf_obj
        assert geom_inp_str == ref_geom_inp_str
        assert grad_inp_str == ref_grad_inp_str
        assert hess_inp_str == ref_hess_inp_str
        assert numpy.isclose(ene, ref_ene)
        assert automol.geom.almost_equal(geo, ref_geo)
        assert numpy.allclose(grad, ref_grad)

    assert len(fs_.conformer.dir.created_names(prefix)) == nconfs


if __name__ == '__main__':
    test__species()
    test__theory()
    # test__conformer()
