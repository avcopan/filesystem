""" conformer filesystem
"""
import os
import numbers
import functools
import numpy
import autofile
import autoinf
from autodir.id_ import is_identifier as _is_identifier
from autodir.id_ import directory_identifiers_at as _directory_identifiers_at
from autodir import par
from autodir import util
from autodir.run import information as _run_information


OPT_RUN_NAME = par.DirectoryName.Run.OPT
GRAD_RUN_NAME = par.DirectoryName.Run.GRAD
HESS_RUN_NAME = par.DirectoryName.Run.HESS


def identifiers(prefix):
    """ list of existing conformer identifiers
    """
    dir_path = base_path(prefix)
    return _directory_identifiers_at(dir_path)


def update_trajectory_file(prefix):
    """ update the trajectory file at this prefix
    """
    rids = identifiers(prefix)
    enes = [read_energy_file(prefix, rid) for rid in rids]
    geos = [read_geometry_file(prefix, rid) for rid in rids]

    # sort them by energy
    srt_idxs = numpy.argsort(enes)
    srt_rids = tuple(map(rids.__getitem__, srt_idxs))
    srt_enes = tuple(map(enes.__getitem__, srt_idxs))
    srt_geos = tuple(map(geos.__getitem__, srt_idxs))
    comments = ["rid: {}, energy: {}".format(rid, str(ene))
                for rid, ene in zip(srt_rids, srt_enes)]
    write_trajectory_file(prefix, srt_geos, comments)


# path definitions
BASE_DIR_NAME = 'CONFS'


def base_path(prefix):
    """ base directory path
    """
    dir_names = (BASE_DIR_NAME,)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def directory_path(prefix, rid):
    """ conformer directory path
    """
    assert _is_identifier(rid)
    prefix = base_path(prefix)
    dir_path = os.path.join(prefix, rid)
    return dir_path


def run_directory_path(prefix, rid):
    """ path to the optimization run directory
    """
    dir_path = directory_path(prefix, rid)
    run_dir_name = par.DirectoryName.RUN
    run_dir_path = os.path.join(dir_path, run_dir_name)
    return run_dir_path


# filesystem create/read/write functions
def create_base(prefix):
    """ create the filesystem base path
    """
    util.create_directory(
        prefix=prefix, dir_path=base_path(prefix))


def create(prefix, rid):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix, dir_path=directory_path(prefix, rid))


def create_run_directory(prefix, rid):
    """ create optimization run directory path
    """
    util.create_directory(
        prefix=prefix, dir_path=run_directory_path(prefix, rid))


# base
def base_information(nsamp, tors_info):
    """ base information object
    """
    tors_info = autoinf.Info(**dict(tors_info))
    assert isinstance(nsamp, numbers.Integral)
    inf_obj = autoinf.Info(nsamp=nsamp, tors_info=tors_info)
    assert autoinf.matches_function_signature(inf_obj, base_information)
    return inf_obj


BASE_INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.CONF),
    dir_path_=base_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=base_information),
)


def base_information_file_path(prefix):
    """ base directory information file path
    """
    return BASE_INFORMATION_FILE.path([prefix])


def has_base_information_file(prefix):
    """ does this filesystem have a base information file?
    """
    return BASE_INFORMATION_FILE.exists([prefix])


def write_base_information_file(prefix, base_inf_obj):
    """ write the base information file to its filesystem path
    """
    BASE_INFORMATION_FILE.write([prefix], base_inf_obj)


def read_base_information_file(prefix):
    """ read the base information file from its filesystem path
    """
    return BASE_INFORMATION_FILE.read([prefix])


# base variable zmatrix
BASE_VMATRIX_FILE = util.DataFile(
    file_name=autofile.name.vmatrix(par.FilePrefix.CONF),
    dir_path_=base_path,
    writer_=autofile.write.vmatrix,
    reader_=autofile.read.vmatrix,
)


def base_vmatrix_file_path(prefix):
    """ base variable information file path
    """
    return BASE_VMATRIX_FILE.path([prefix])


def has_base_vmatrix_file(prefix):
    """ does this filesystem have a base variable information file?
    """
    return BASE_VMATRIX_FILE.exists([prefix])


def write_base_vmatrix_file(prefix, base_inf_obj):
    """ write the base variable information file to its filesystem path
    """
    BASE_VMATRIX_FILE.write([prefix], base_inf_obj)


def read_base_vmatrix_file(prefix):
    """ read the base variable information file from its filesystem path
    """
    return BASE_VMATRIX_FILE.read([prefix])


# geometry files
# # information file
INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.GEOM),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=_run_information),
)


def information_file_path(prefix, rid):
    """ gradient information file path
    """
    return INFORMATION_FILE.path([prefix, rid])


def has_information_file(prefix, rid):
    """ does this filesystem have a gradient information file?
    """
    return INFORMATION_FILE.exists([prefix, rid])


def write_information_file(prefix, rid, grad_inp_str):
    """ write the gradient information file to its filesystem path
    """
    INFORMATION_FILE.write([prefix, rid], grad_inp_str)


def read_information_file(prefix, rid):
    """ read the gradient information file from its filesystem path
    """
    return INFORMATION_FILE.read([prefix, rid])


# # input file
INPUT_FILE = util.DataFile(
    file_name=autofile.name.input_file(par.FilePrefix.GEOM),
    dir_path_=directory_path,
)


def input_file_path(prefix, rid):
    """ input file path
    """
    return INPUT_FILE.path([prefix, rid])


def has_input_file(prefix, rid):
    """ does this filesystem have a input file?
    """
    return INPUT_FILE.exists([prefix, rid])


def write_input_file(prefix, rid, inp_str):
    """ write the input file to its filesystem path
    """
    INPUT_FILE.write([prefix, rid], inp_str)


def read_input_file(prefix, rid):
    """ read the input file from its filesystem path
    """
    return INPUT_FILE.read([prefix, rid])


# # geometry file
GEOMETRY_FILE = util.DataFile(
    file_name=autofile.name.geometry(par.FilePrefix.GEOM),
    dir_path_=directory_path,
    writer_=autofile.write.geometry,
    reader_=autofile.read.geometry,
)


def geometry_file_path(prefix, rid):
    """ geometry file path
    """
    return GEOMETRY_FILE.path([prefix, rid])


def has_geometry_file(prefix, rid):
    """ does this filesystem have a geometry file?
    """
    return GEOMETRY_FILE.exists([prefix, rid])


def write_geometry_file(prefix, rid, geo):
    """ write the geometry file to its filesystem path
    """
    GEOMETRY_FILE.write([prefix, rid], geo)


def read_geometry_file(prefix, rid):
    """ read the geometry file from its filesystem path
    """
    return GEOMETRY_FILE.read([prefix, rid])


# # the energy file
ENERGY_FILE = util.DataFile(
    file_name=autofile.name.energy(par.FilePrefix.GEOM),
    dir_path_=directory_path,
    writer_=autofile.write.energy,
    reader_=autofile.read.energy,
)


def energy_file_path(prefix, rid):
    """ energy file path
    """
    return ENERGY_FILE.path([prefix, rid])


def has_energy_file(prefix, rid):
    """ does this filesystem have a energy file?
    """
    return ENERGY_FILE.exists([prefix, rid])


def write_energy_file(prefix, rid, ene):
    """ write the energy file to its filesystem path
    """
    ENERGY_FILE.write([prefix, rid], ene)


def read_energy_file(prefix, rid):
    """ read the energy file from its filesystem path
    """
    return ENERGY_FILE.read([prefix, rid])


# gradient
# # the gradient information file
GRADIENT_INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.GRAD),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=_run_information),
)


def gradient_information_file_path(prefix, rid):
    """ gradient information file path
    """
    return GRADIENT_INFORMATION_FILE.path([prefix, rid])


def has_gradient_information_file(prefix, rid):
    """ does this filesystem have a gradient information file?
    """
    return GRADIENT_INFORMATION_FILE.exists([prefix, rid])


def write_gradient_information_file(prefix, rid, grad_inp_str):
    """ write the gradient information file to its filesystem path
    """
    GRADIENT_INFORMATION_FILE.write([prefix, rid], grad_inp_str)


def read_gradient_information_file(prefix, rid):
    """ read the gradient information file from its filesystem path
    """
    return GRADIENT_INFORMATION_FILE.read([prefix, rid])


# # gradient input file
GRADIENT_INPUT_FILE = util.DataFile(
    file_name=autofile.name.input_file(par.FilePrefix.GRAD),
    dir_path_=directory_path,
)


def gradient_input_file_path(prefix, rid):
    """ gradient input file path
    """
    return GRADIENT_INPUT_FILE.path([prefix, rid])


def has_gradient_input_file(prefix, rid):
    """ does this filesystem have a gradient input file?
    """
    return GRADIENT_INPUT_FILE.exists([prefix, rid])


def write_gradient_input_file(prefix, rid, grad_inp_str):
    """ write the gradient input file to its filesystem path
    """
    GRADIENT_INPUT_FILE.write([prefix, rid], grad_inp_str)


def read_gradient_input_file(prefix, rid):
    """ read the gradient input file from its filesystem path
    """
    return GRADIENT_INPUT_FILE.read([prefix, rid])


# # the gradient file
GRADIENT_FILE = util.DataFile(
    file_name=autofile.name.gradient(par.FilePrefix.GRAD),
    dir_path_=directory_path,
    writer_=autofile.write.gradient,
    reader_=autofile.read.gradient,
)


def gradient_file_path(prefix, rid):
    """ gradient file path
    """
    return GRADIENT_FILE.path([prefix, rid])


def has_gradient_file(prefix, rid):
    """ does this filesystem have a gradient file?
    """
    return GRADIENT_FILE.exists([prefix, rid])


def write_gradient_file(prefix, rid, ene):
    """ write the gradient file to its filesystem path
    """
    GRADIENT_FILE.write([prefix, rid], ene)


def read_gradient_file(prefix, rid):
    """ read the gradient file from its filesystem path
    """
    return GRADIENT_FILE.read([prefix, rid])


# hessian
# # the hessian information file
HESSIAN_INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.HESS),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=_run_information),
)


def hessian_information_file_path(prefix, rid):
    """ hessian information file path
    """
    return HESSIAN_INFORMATION_FILE.path([prefix, rid])


def has_hessian_information_file(prefix, rid):
    """ does this filesystem have a hessian information file?
    """
    return HESSIAN_INFORMATION_FILE.exists([prefix, rid])


def write_hessian_information_file(prefix, rid, grad_inp_str):
    """ write the hessian information file to its filesystem path
    """
    HESSIAN_INFORMATION_FILE.write([prefix, rid], grad_inp_str)


def read_hessian_information_file(prefix, rid):
    """ read the hessian information file from its filesystem path
    """
    return HESSIAN_INFORMATION_FILE.read([prefix, rid])


# # hessian input file
HESSIAN_INPUT_FILE = util.DataFile(
    file_name=autofile.name.input_file(par.FilePrefix.HESS),
    dir_path_=directory_path,
)


def hessian_input_file_path(prefix, rid):
    """ hessian input file path
    """
    return HESSIAN_INPUT_FILE.path([prefix, rid])


def has_hessian_input_file(prefix, rid):
    """ does this filesystem have a hessian input file?
    """
    return HESSIAN_INPUT_FILE.exists([prefix, rid])


def write_hessian_input_file(prefix, rid, grad_inp_str):
    """ write the hessian input file to its filesystem path
    """
    HESSIAN_INPUT_FILE.write([prefix, rid], grad_inp_str)


def read_hessian_input_file(prefix, rid):
    """ read the hessian input file from its filesystem path
    """
    return HESSIAN_INPUT_FILE.read([prefix, rid])


# # the hessian file
HESSIAN_FILE = util.DataFile(
    file_name=autofile.name.hessian(par.FilePrefix.HESS),
    dir_path_=directory_path,
    writer_=autofile.write.hessian,
    reader_=autofile.read.hessian,
)


def hessian_file_path(prefix, rid):
    """ hessian file path
    """
    return HESSIAN_FILE.path([prefix, rid])


def has_hessian_file(prefix, rid):
    """ does this filesystem have a hessian file?
    """
    return HESSIAN_FILE.exists([prefix, rid])


def write_hessian_file(prefix, rid, ene):
    """ write the hessian file to its filesystem path
    """
    HESSIAN_FILE.write([prefix, rid], ene)


def read_hessian_file(prefix, rid):
    """ read the hessian file from its filesystem path
    """
    return HESSIAN_FILE.read([prefix, rid])


# # trajectory file
def _raise_not_implemented(*args, **kwargs):
    """ dummy function to raise NotImplementedError and quit """
    assert args or not args or kwargs or not kwargs
    raise NotImplementedError


TRAJECTORY_FILE = util.DataFile(
    file_name=autofile.name.trajectory(par.FilePrefix.CONF),
    dir_path_=base_path,
    writer_=(lambda args: autofile.write.trajectory(*args)),
    reader_=_raise_not_implemented,
)


def trajectory_file_path(prefix):
    """ base directory information file path
    """
    return TRAJECTORY_FILE.path([prefix])


def has_trajectory_file(prefix):
    """ does this filesystem have a base information file?
    """
    return TRAJECTORY_FILE.exists([prefix])


def write_trajectory_file(prefix, geos, comments):
    """ write the base information file to its filesystem path
    """
    TRAJECTORY_FILE.write([prefix], [geos, comments])


def read_trajectory_file(prefix):
    """ read the base information file from its filesystem path
    """
    return TRAJECTORY_FILE.read([prefix])
