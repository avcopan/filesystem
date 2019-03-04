""" theory filesystem
"""
import os


# filesystem create/read/write functions
def create(prefix, method, basis=None):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, method, basis)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# path definitions
def directory_path(prefix, method, basis=None):
    """ filesystem directory path
    """
    if basis is None:
        theory = composite_name(method)
    else:
        theory = standard_name(method, basis)

    dir_path = os.path.join(prefix, theory)
    return dir_path


# standard theory naming
class BASIS():
    """ electronic structure basis sets """
    STO3G = 'STO-3G'
    P321G = '3-21G'
    P631G = '6-31G'
    PVDZ = 'PVDZ'
    PVTZ = 'PVTZ'


class METHOD():
    """ electronic structure method """

    RHF = 'RHF'
    UHF = 'UHF'
    RHF_MP2 = 'RHF-MP2'
    UHF_MP2 = 'UHF-MP2'


BASES = (BASIS.STO3G, BASIS.P321G, BASIS.P631G, BASIS.PVDZ, BASIS.PVTZ)
METHODS = (METHOD.RHF, METHOD.UHF, METHOD.RHF_MP2, METHOD.UHF_MP2)


def standard_name(method, basis):
    """ standard theory name from method and basis
    """
    method = str(method).upper()
    basis = str(basis).upper()
    assert basis in BASES
    assert method in METHODS
    return '{}_{}'.format(method, basis)


def composite_name(method):
    """ theory name for a composite method
    """
    raise NotImplementedError(method)
