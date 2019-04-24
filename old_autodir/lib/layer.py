""" DataLayers
"""
import automol
import autodir.lib
from autodir import factory


class FilePrefix():
    """ file prefixes """
    INFO = 'info'
    CONF = 'conf'
    GEOM = 'geom'
    GRAD = 'grad'
    HESS = 'hess'


class DataFileAttributeName():
    """ DataFile attribute names """
    INFO = 'info'
    VMATRIX = 'vmatrix'
    GEOM_INFO = 'geometry_information'
    GRAD_INFO = 'gradient_information'
    HESS_INFO = 'hessian_information'
    GEOM_INPUT = 'geometry_input'
    GRAD_INPUT = 'gradient_input'
    HESS_INPUT = 'hessian_input'
    ENERGY = 'energy'
    GEOM = 'geometry'
    GRAD = 'gradient'
    HESS = 'hessian'


# data layer generators
def species_trunk():
    """ species trunk DataLayer
    """
    ddir = autodir.lib.dir_.species_trunk()
    return factory.DataLayer(ddir=ddir)


def species_leaf():
    """ species leaf DataLayer
    """
    ddir = autodir.lib.dir_.species_leaf()
    inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.INFO, function=autodir.lib.info.species_leaf)

    # automatically write the information file when we create the directory
    def creation_side_effect_(prefix, args):
        ich, mult = args
        smi = automol.inchi.smiles(ich)
        inf_obj = autodir.lib.info.species_leaf(
            inchi=ich, smiles=smi, mult=mult)
        inf_dfile.write(inf_obj, prefix, args)
    ddir.creation_side_effect_ = creation_side_effect_

    dlayer = factory.DataLayer(
        ddir=ddir,
        dfile_dct={
            DataFileAttributeName.INFO: inf_dfile})
    return dlayer


def theory_leaf():
    """ theory leaf DataLayer
    """
    ddir = autodir.lib.dir_.theory_leaf()
    inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.INFO, function=autodir.lib.info.theory_leaf)

    # automatically write the information file when we create the directory
    def creation_side_effect_(prefix, args):
        method, basis, orb_restricted = args
        inf_obj = autodir.lib.info.theory_leaf(
            method=method, basis=basis, orb_restricted=orb_restricted)
        inf_dfile.write(inf_obj, prefix, args)
    ddir.creation_side_effect_ = creation_side_effect_

    dlayer = factory.DataLayer(
        ddir=ddir,
        dfile_dct={
            DataFileAttributeName.INFO: inf_dfile})
    return dlayer


def conformer_trunk():
    """ conformer trunk DataLayer
    """
    ddir = autodir.lib.dir_.conformer_trunk()
    vma_dfile = autodir.lib.file_.vmatrix(ddir, FilePrefix.CONF)
    inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.CONF, function=autodir.lib.info.conformer_trunk)

    dlayer = factory.DataLayer(
        ddir=ddir,
        dfile_dct={
            DataFileAttributeName.VMATRIX: vma_dfile,
            DataFileAttributeName.INFO: inf_dfile})
    return dlayer


def conformer_leaf():
    """ conformer leaf DataLayer
    """
    ddir = autodir.lib.dir_.conformer_leaf()
    geom_inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.GEOM, function=autodir.lib.info.run)
    grad_inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.GRAD, function=autodir.lib.info.run)
    hess_inf_dfile = autodir.lib.file_.information(
        ddir, FilePrefix.HESS, function=autodir.lib.info.run)
    geom_inp_dfile = autodir.lib.file_.input_file(ddir, FilePrefix.GEOM)
    grad_inp_dfile = autodir.lib.file_.input_file(ddir, FilePrefix.GRAD)
    hess_inp_dfile = autodir.lib.file_.input_file(ddir, FilePrefix.HESS)
    ene_dfile = autodir.lib.file_.energy(ddir, FilePrefix.GEOM)
    geom_dfile = autodir.lib.file_.geometry(ddir, FilePrefix.GEOM)
    grad_dfile = autodir.lib.file_.gradient(ddir, FilePrefix.GRAD)
    hess_dfile = autodir.lib.file_.hessian(ddir, FilePrefix.HESS)

    dlayer = factory.DataLayer(
        ddir=ddir,
        dfile_dct={
            DataFileAttributeName.GEOM_INFO: geom_inf_dfile,
            DataFileAttributeName.GRAD_INFO: grad_inf_dfile,
            DataFileAttributeName.HESS_INFO: hess_inf_dfile,
            DataFileAttributeName.GEOM_INPUT: geom_inp_dfile,
            DataFileAttributeName.GRAD_INPUT: grad_inp_dfile,
            DataFileAttributeName.HESS_INPUT: hess_inp_dfile,
            DataFileAttributeName.ENERGY: ene_dfile,
            DataFileAttributeName.GEOM: geom_dfile,
            DataFileAttributeName.GRAD: grad_dfile,
            DataFileAttributeName.HESS: hess_dfile})
    return dlayer
