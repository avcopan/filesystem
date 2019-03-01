""" theory filesystem
"""
import os


class BASIS():
    """ electronic structure basis sets """
    STO3G = 'STO-3G'
    P321G = '3-21G'
    P631G = '6-31G'
    PVDZ = 'CC-PVDZ'
    PVTZ = 'CC-PVTZ'


class METHOD():
    """ electronic structure method """

    RHF = 'RHF'
    UHF = 'UHF'
    RHF_MP2 = 'RHF-MP2'
    UHF_MP2 = 'UHF-MP2'


BASES = (BASIS.STO3G, BASIS.P321G, BASIS.P631G, BASIS.PVDZ, BASIS.PVTZ)
METHODS = (METHOD.RHF, METHOD.UHF, METHOD.RHF_MP2, METHOD.UHF_MP2)


def schema(method, basis):
    """ theory directory schema

    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: int
    :returns: a directory path and a dictionary of file strings by file path
    :rtype: (str, dict)
    """
    method = str(method).upper()
    basis = str(basis).upper()
    assert basis in BASES
    assert method in METHODS
    dir_names = (method, basis)
    dir_path = os.path.join(*dir_names)
    file_spec_dct = {}
    return dir_path, file_spec_dct
