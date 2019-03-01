""" lennard-jones filesystem
"""
import os
import autofile
from .params import PREFIX as _PREFIX

BASE_DIR_NAME = 'LJ'


class BATHxGAS():
    """ bath gas """
    N2 = 'N2'
    HE = 'HE'
    NE = 'NE'
    AR = 'AR'
    KR = 'KR'


class METHOD():
    """ lennard-jones method """
    LJ126 = 'LJ126'
    BUCK = 'BUCK'
    REAL = 'REAL'


class INFO():
    """ parameters for the information dictionary
    """
    NSAMP_KEY = 'nsamples'


BATH_GASES = (BATHxGAS.N2, BATHxGAS.HE, BATHxGAS.NE, BATHxGAS.KR)
METHODS = (METHOD.LJ126, METHOD.BUCK, METHOD.REAL)


def schema(bath_gas, method, geo, bath_geo, eps, sig, nsamp):
    """ lennard-jones directory schema
    """
    bath_gas = str(bath_gas).upper()
    method = str(method).upper()
    assert bath_gas in BATH_GASES
    assert method in METHODS
    dir_names = (BASE_DIR_NAME, bath_gas, method)
    dir_path = os.path.join(*dir_names)

    file_spec_dct = dict([
        _information_file_spec(dir_path, nsamp),
        _geometry_file_spec(dir_path, geo, _PREFIX.MAIN),
        _geometry_file_spec(dir_path, bath_geo, _PREFIX.BATH),
        _epsilon_file_spec(dir_path, eps),
        _sigma_file_spec(dir_path, sig),
    ])
    return dir_path, file_spec_dct


def _information_file_spec(dir_path, nsamp):
    assert isinstance(nsamp, int)
    inf_dct = {INFO.NSAMP_KEY: nsamp}

    file_str = autofile.write.information(inf_dct)
    file_name = autofile.name.information(_PREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return (file_path, file_str)


def _geometry_file_spec(dir_path, geo, prefix):
    file_str = autofile.write.geometry(geo)
    file_name = autofile.name.geometry(prefix)
    file_path = os.path.join(dir_path, file_name)
    return (file_path, file_str)


def _epsilon_file_spec(dir_path, eps):
    file_str = autofile.write.lennard_jones_epsilon(eps)
    file_name = autofile.name.lennard_jones_epsilon(_PREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return (file_path, file_str)


def _sigma_file_spec(dir_path, sig):
    file_str = autofile.write.lennard_jones_sigma(sig)
    file_name = autofile.name.lennard_jones_sigma(_PREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return (file_path, file_str)
