""" theory filesystem
"""
import os
import base64
import hashlib
import elstruct
import autoinf
import autofile
from autodir.params import FILExPREFIX as _FILExPREFIX


# filesystem create/read/write functions
def create(prefix, method, basis, open_shell, orb_restricted):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, method, basis, open_shell,
                              orb_restricted)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write the information file
    inf_obj = information(method, basis, open_shell, orb_restricted)
    inf_str = autofile.write.information(inf_obj)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    autofile.write_file(file_path, inf_str)


def directory_path(prefix, method, basis, open_shell, orb_restricted):
    """ theory directory path
    """
    assert os.path.isdir(prefix)
    dir_name = directory_name(method, basis, open_shell, orb_restricted)
    dir_path = os.path.join(prefix, dir_name)
    return dir_path


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

    basis_hash = _short_hash(basis)
    method_hash = _short_hash(method)
    ref_char = 'R' if orb_restricted else 'U'
    dir_name = ''.join([method_hash, basis_hash, ref_char])
    return dir_name


def _short_hash(string):
    string = string.lower().encode('utf-8')
    dig = hashlib.md5(string).digest()
    hsh = base64.urlsafe_b64encode(dig)[:3]
    return hsh.decode()


# information files
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
