""" electronic structure run filesystem
"""
import os
import datetime
import functools
import autoinf
import autofile
from autodir import par
from autodir import util


# path definitions
def directory_path(prefix, name):
    """ run directory path
    """
    assert isinstance(name, str)
    dir_path = os.path.join(prefix, name)
    return dir_path


# filesystem create/read/writer functions
def create(prefix, name):
    """ create the filesystem path
    """
    util.create_directory(prefix=prefix, dir_path=directory_path(prefix, name))


# # information
def information(job, prog, method, basis, utc_start_time=None,
                utc_end_time=None):
    """ base information object
    """
    inf_obj = autoinf.Info(
        job=job,
        prog=prog,
        method=method,
        basis=basis,
        utc_start_time=utc_start_time,
        utc_end_time=utc_end_time,
    )
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj


def add_start_time_to_information(inf_obj):
    """ add start time to the information object
    """
    inf_obj.utc_start_time = datetime.datetime.utcnow()


def add_end_time_to_information(inf_obj):
    """ add start time to the information object
    """
    inf_obj.utc_end_time = datetime.datetime.utcnow()


INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.INFO),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=information),
)


def information_file_path(prefix, name):
    """ gradient information file path
    """
    return INFORMATION_FILE.path([prefix, name])


def has_information_file(prefix, name):
    """ does this filesystem have a gradient information file?
    """
    return INFORMATION_FILE.exists([prefix, name])


def write_information_file(prefix, name, grad_inp_str):
    """ write the gradient information file to its filesystem path
    """
    INFORMATION_FILE.write([prefix, name], grad_inp_str)


def read_information_file(prefix, name):
    """ read the gradient information file from its filesystem path
    """
    return INFORMATION_FILE.read([prefix, name])


# # input file
INPUT_FILE = util.DataFile(
    file_name=autofile.name.input_file(par.FilePrefix.RUN),
    dir_path_=directory_path,
)


def input_file_path(prefix, name):
    """ input file path
    """
    return INPUT_FILE.path([prefix, name])


def has_input_file(prefix, name):
    """ does this filesystem have a input file?
    """
    return INPUT_FILE.exists([prefix, name])


def write_input_file(prefix, name, inp_str):
    """ write the input file to its filesystem path
    """
    INPUT_FILE.write([prefix, name], inp_str)


def read_input_file(prefix, name):
    """ read the input file from its filesystem path
    """
    return INPUT_FILE.read([prefix, name])


# # output file
OUTPUT_FILE = util.DataFile(
    file_name=autofile.name.output_file(par.FilePrefix.RUN),
    dir_path_=directory_path,
)


def output_file_path(prefix, name):
    """ output file path
    """
    return OUTPUT_FILE.path([prefix, name])


def has_output_file(prefix, name):
    """ does this filesystem have a output file?
    """
    return OUTPUT_FILE.exists([prefix, name])


def write_output_file(prefix, name, inp_str):
    """ write the output file to its filesystem path
    """
    OUTPUT_FILE.write([prefix, name], inp_str)


def read_output_file(prefix, name):
    """ read the output file from its filesystem path
    """
    return OUTPUT_FILE.read([prefix, name])
