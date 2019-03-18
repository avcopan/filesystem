""" electronic structure run filesystem
"""
import os
import autoinf
import autofile
from autodir.id_ import is_identifier as _is_identifier
from autodir.id_ import directory_identifiers_at as _directory_identifiers_at
from autodir.params import FILExPREFIX as _FILExPREFIX


def identifiers(prefix):
    """ list of existing identifiers
    """
    dir_path = base_path(prefix)
    return _directory_identifiers_at(dir_path)


# filesystem create/read/writer functions
def create_base(prefix):
    """ create the filesystem base path
    """
    dir_path = base_path(prefix)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def create(prefix, rid):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, rid)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def has_base_information_file(prefix):
    """ does this filesystem have a base information file?
    """
    file_path = base_information_file_path(prefix)
    return os.path.isfile(file_path)


def write_base_information_file(prefix, base_inf_obj):
    """ write the base information file to its filesystem path
    """
    assert autoinf.matches_function_signature(base_inf_obj, base_information)
    file_path = base_information_file_path(prefix)
    file_str = autofile.write.information(base_inf_obj)
    autofile.write_file(file_path, file_str)


def read_base_information_file(prefix):
    """ read the base information file from its filesystem path
    """
    file_path = base_information_file_path(prefix)
    file_str = autofile.read_file(file_path)
    base_inf_obj = autofile.read.information(file_str)
    assert autoinf.matches_function_signature(base_inf_obj, base_information)
    return base_inf_obj


def write_run_script(prefix, scr_str):
    """ write the run script to its filesystem path
    """
    file_path = run_script_path(prefix)
    autofile.write_file(file_path, scr_str)


def read_run_script(prefix):
    """ read the run script from its filesystem path
    """
    file_path = run_script_path(prefix)
    scr_str = autofile.read_file(file_path)
    return scr_str


def write_input_file(prefix, rid, inp_str):
    """ read the input file from its filesystem path
    """
    file_path = input_file_path(prefix, rid)
    autofile.write_file(file_path, inp_str)


def read_input_file(prefix, rid):
    """ read the input file from its filesystem path
    """
    file_path = input_file_path(prefix, rid)
    inp_str = autofile.read_file(file_path)
    return inp_str


def write_output_file(prefix, rid, out_str):
    """ read the output file from its filesystem path
    """
    file_path = output_file_path(prefix, rid)
    autofile.write_file(file_path, out_str)


def read_output_file(prefix, rid):
    """ read the output file from its filesystem path
    """
    file_path = output_file_path(prefix, rid)
    out_str = autofile.read_file(file_path)
    return out_str


def write_geometry_file(prefix, rid, geo):
    """ write the geometry file to its filesystem path
    """
    file_path = geometry_file_path(prefix, rid)
    file_str = autofile.write.geometry(geo)
    autofile.write_file(file_path, file_str)


def read_geometry_file(prefix, rid):
    """ read the geometry file from its filesystem path
    """
    file_path = geometry_file_path(prefix, rid)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.geometry(file_str)
    return geo


# path definitions
BASE_DIR_NAME = 'RUNS'


def base_path(prefix):
    """ base directory path
    """
    assert os.path.isdir(prefix)
    dir_names = (BASE_DIR_NAME,)
    dir_pth = os.path.join(prefix, *dir_names)
    return dir_pth


def directory_path(prefix, rid):
    """ run directory path
    """
    assert _is_identifier(rid)
    base_pth = base_path(prefix)
    dir_pth = os.path.join(base_pth, rid)
    return dir_pth


def base_information_file_path(prefix):
    """ base directory information file path
    """
    dir_path = base_path(prefix)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def run_script_path(prefix):
    """ run script path
    """
    dir_pth = base_path(prefix)
    file_name = autofile.name.run_script(_FILExPREFIX.RUN)
    file_pth = os.path.join(dir_pth, file_name)
    return file_pth


def input_file_path(prefix, rid):
    """ run input file path
    """
    dir_pth = directory_path(prefix, rid)
    file_name = autofile.name.input_file(_FILExPREFIX.RUN)
    file_pth = os.path.join(dir_pth, file_name)
    return file_pth


def output_file_path(prefix, rid):
    """ run output file path
    """
    dir_pth = directory_path(prefix, rid)
    file_name = autofile.name.output_file(_FILExPREFIX.RUN)
    file_pth = os.path.join(dir_pth, file_name)
    return file_pth


def geometry_file_path(prefix, rid):
    """ filesystem geometry file path
    """
    dir_path = directory_path(prefix, rid)
    file_name = autofile.name.geometry(_FILExPREFIX.RUN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


# information files
def base_information(function, function_info, job, prog, method, basis,
                     inchi, complete):
    """ base information object
    """
    assert isinstance(function_info, autoinf.Info)
    inf_obj = autoinf.Info(function=function,
                           function_info=function_info, job=job,
                           prog=prog, method=method, basis=basis,
                           inchi=inchi, complete=complete)
    assert autoinf.matches_function_signature(inf_obj, base_information)
    return inf_obj
