""" theory filesystem
"""
import os
import base64
import hashlib
import functools
import elstruct
import autoinf
import autofile
from autodir import par
from autodir import util


def short_hash(string):
    """ determine a short (3-character) hash from a string
    """
    string = string.lower().encode('utf-8')
    dig = hashlib.md5(string).digest()
    hsh = base64.urlsafe_b64encode(dig)[:3]
    return hsh.decode()


def directory_name(method, basis, open_shell, orb_restricted):
    """ determine the name for the directory
    """
    method = elstruct.par.Method.standard_case(method)
    basis = elstruct.par.Method.standard_case(basis)
    assert isinstance(open_shell, bool)
    assert isinstance(orb_restricted, bool)

    if not open_shell:
        assert orb_restricted is True
    else:
        if elstruct.par.Method.is_dft(method):
            assert orb_restricted is False if open_shell else orb_restricted

    basis_hash = short_hash(basis)
    method_hash = short_hash(method)
    ref_char = 'R' if orb_restricted else 'U'
    dir_name = ''.join([method_hash, basis_hash, ref_char])
    return dir_name


# path definitions
def directory_path(prefix, method, basis, open_shell, orb_restricted):
    """ theory directory path
    """
    dir_name = directory_name(method, basis, open_shell, orb_restricted)
    dir_path = os.path.join(prefix, dir_name)
    return dir_path


# filesystem create/read/write functions
def create(prefix, method, basis, open_shell, orb_restricted):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix,
        dir_path=directory_path(prefix, method, basis, open_shell,
                                orb_restricted))

    # write the information file
    inf_obj = information(method, basis, open_shell, orb_restricted)
    write_information_file(
        prefix, method, basis, open_shell, orb_restricted, inf_obj)


# # information
def information(method, basis, open_shell, orb_restricted):
    """ information object
    """
    method = elstruct.par.Method.standard_case(method)
    basis = elstruct.par.Method.standard_case(basis)
    assert isinstance(open_shell, bool)
    assert isinstance(orb_restricted, bool)
    inf_obj = autoinf.Info(method=method, basis=basis, open_shell=open_shell,
                           orb_restricted=orb_restricted)
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj


INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.INFO),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=information),
)


def information_file_path(prefix, method, basis, open_shell, orb_restricted):
    """ information file path
    """
    return INFORMATION_FILE.path(
        [prefix, method, basis, open_shell, orb_restricted])


def has_information_file(prefix, method, basis, open_shell, orb_restricted):
    """ does this filesystem have an information file?
    """
    return INFORMATION_FILE.exists(
        [prefix, method, basis, open_shell, orb_restricted])


def write_information_file(prefix, method, basis, open_shell, orb_restricted,
                           inf_obj):
    """ write the information file to its filesystem path
    """
    INFORMATION_FILE.write(
        [prefix, method, basis, open_shell, orb_restricted], inf_obj)


def read_information_file(prefix, method, basis, open_shell, orb_restricted):
    """ read the information file from its filesystem path
    """
    return INFORMATION_FILE.read(
        [prefix, method, basis, open_shell, orb_restricted])
