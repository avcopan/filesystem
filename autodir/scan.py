""" scan filesystem

tors_dct: {coordinate name: number of points}
"""
import os
import functools
import autofile
import autoinf
from autodir import par
from autodir import util
from autodir.run import information as _run_information


# path definitions
BASE_DIR_NAME = 'SCANS'


def base_path(prefix):
    """ base directory path
    """
    dir_names = (BASE_DIR_NAME,)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def scan_path(prefix, tors_dct):
    """ scan directory path
    """
    prefix = base_path(prefix)
    dir_name = '_'.join(sorted(tors_dct))
    dir_path = os.path.join(prefix, dir_name)
    return dir_path


def directory_path(prefix, tors_dct, idxs):
    """ scan entry directory path
    """
    assert all(idx in idx_range
               for idx, idx_range in zip(idxs, _index_ranges(tors_dct)))
    prefix = scan_path(prefix, tors_dct)
    dir_name = '_'.join(map('{:0>2d}'.format, idxs))
    dir_path = os.path.join(prefix, dir_name)
    return dir_path


def _index_ranges(tors_dct):
    return list(map(range, map(tors_dct.__getitem__, sorted(tors_dct))))


def run_directory_path(prefix, tors_dct, idxs):
    """ path to the optimization run directory
    """
    dir_path = directory_path(prefix, tors_dct, idxs)
    run_dir_name = par.DirectoryName.RUN
    run_dir_path = os.path.join(dir_path, run_dir_name)
    return run_dir_path


# filesystem create/read/write functions
def create_base(prefix):
    """ create the filesystem base path
    """
    util.create_directory(
        prefix=prefix, dir_path=base_path(prefix))


def create_scan(prefix, tors_dct):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix, dir_path=scan_path(prefix, tors_dct))


def create(prefix, tors_dct, idxs):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix, dir_path=directory_path(prefix, tors_dct, idxs))


def create_run_directory(prefix, tors_dct, idxs):
    """ create optimization run directory path
    """
    util.create_directory(
        prefix=prefix, dir_path=run_directory_path(prefix, tors_dct, idxs))


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


def information_file_path(prefix, tors_dct, idxs):
    """ gradient information file path
    """
    return INFORMATION_FILE.path([prefix, tors_dct, idxs])


def has_information_file(prefix, tors_dct, idxs):
    """ does this filesystem have a gradient information file?
    """
    return INFORMATION_FILE.exists([prefix, tors_dct, idxs])


def write_information_file(prefix, tors_dct, idxs, grad_inp_str):
    """ write the gradient information file to its filesystem path
    """
    INFORMATION_FILE.write([prefix, tors_dct, idxs], grad_inp_str)


def read_information_file(prefix, tors_dct, idxs):
    """ read the gradient information file from its filesystem path
    """
    return INFORMATION_FILE.read([prefix, tors_dct, idxs])


# # input file
INPUT_FILE = util.DataFile(
    file_name=autofile.name.input_file(par.FilePrefix.GEOM),
    dir_path_=directory_path,
)


def input_file_path(prefix, tors_dct, idxs):
    """ input file path
    """
    return INPUT_FILE.path([prefix, tors_dct, idxs])


def has_input_file(prefix, tors_dct, idxs):
    """ does this filesystem have a input file?
    """
    return INPUT_FILE.exists([prefix, tors_dct, idxs])


def write_input_file(prefix, tors_dct, idxs, inp_str):
    """ write the input file to its filesystem path
    """
    INPUT_FILE.write([prefix, tors_dct, idxs], inp_str)


def read_input_file(prefix, tors_dct, idxs):
    """ read the input file from its filesystem path
    """
    return INPUT_FILE.read([prefix, tors_dct, idxs])


# # geometry file
GEOMETRY_FILE = util.DataFile(
    file_name=autofile.name.geometry(par.FilePrefix.GEOM),
    dir_path_=directory_path,
    writer_=autofile.write.geometry,
    reader_=autofile.read.geometry,
)


def geometry_file_path(prefix, tors_dct, idxs):
    """ geometry file path
    """
    return GEOMETRY_FILE.path([prefix, tors_dct, idxs])


def has_geometry_file(prefix, tors_dct, idxs):
    """ does this filesystem have a geometry file?
    """
    return GEOMETRY_FILE.exists([prefix, tors_dct, idxs])


def write_geometry_file(prefix, tors_dct, idxs, geo):
    """ write the geometry file to its filesystem path
    """
    GEOMETRY_FILE.write([prefix, tors_dct, idxs], geo)


def read_geometry_file(prefix, tors_dct, idxs):
    """ read the geometry file from its filesystem path
    """
    return GEOMETRY_FILE.read([prefix, tors_dct, idxs])


# # the energy file
ENERGY_FILE = util.DataFile(
    file_name=autofile.name.energy(par.FilePrefix.GEOM),
    dir_path_=directory_path,
    writer_=autofile.write.energy,
    reader_=autofile.read.energy,
)


def energy_file_path(prefix, tors_dct, idxs):
    """ energy file path
    """
    return ENERGY_FILE.path([prefix, tors_dct, idxs])


def has_energy_file(prefix, tors_dct, idxs):
    """ does this filesystem have a energy file?
    """
    return ENERGY_FILE.exists([prefix, tors_dct, idxs])


def write_energy_file(prefix, tors_dct, idxs, ene):
    """ write the energy file to its filesystem path
    """
    ENERGY_FILE.write([prefix, tors_dct, idxs], ene)


def read_energy_file(prefix, tors_dct, idxs):
    """ read the energy file from its filesystem path
    """
    return ENERGY_FILE.read([prefix, tors_dct, idxs])
