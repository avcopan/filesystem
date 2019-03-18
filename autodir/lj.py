""" lennard-jones filesystem
"""
import os
import numbers
import autoinf
import autofile
from autodir.params import FILExPREFIX as _FILExPREFIX


# filesystem create/read/write functions
def create(prefix, bath, pot):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, bath, pot)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_geometry_file(prefix, bath, pot, geo):
    """ write the geometry file to its filesystem path
    """
    file_path = geometry_file_path(prefix, bath, pot)
    file_str = autofile.write.geometry(geo)
    autofile.write_file(file_path, file_str)


def read_geometry_file(prefix, bath, pot):
    """ read the geometry file from its filesystem path
    """
    file_path = geometry_file_path(prefix, bath, pot)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.geometry(file_str)
    return geo


def write_bath_geometry_file(prefix, bath, pot, geo):
    """ write the bath geometry file to its filesystem path
    """
    file_path = bath_geometry_file_path(prefix, bath, pot)
    file_str = autofile.write.geometry(geo)
    autofile.write_file(file_path, file_str)


def read_bath_geometry_file(prefix, bath, pot):
    """ read the bath geometry file from its filesystem path
    """
    file_path = bath_geometry_file_path(prefix, bath, pot)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.geometry(file_str)
    return geo


def write_epsilon_file(prefix, bath, pot, geo):
    """ write the lennard-jones epsilon file to its filesystem path
    """
    file_path = epsilon_file_path(prefix, bath, pot)
    file_str = autofile.write.lennard_jones_epsilon(geo)
    autofile.write_file(file_path, file_str)


def read_epsilon_file(prefix, bath, pot):
    """ read the lennard-jones epsilon file from its filesystem path
    """
    file_path = epsilon_file_path(prefix, bath, pot)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.lennard_jones_epsilon(file_str)
    return geo


def write_sigma_file(prefix, bath, pot, geo):
    """ write the lennard-jones sigma file to its filesystem path
    """
    file_path = sigma_file_path(prefix, bath, pot)
    file_str = autofile.write.lennard_jones_sigma(geo)
    autofile.write_file(file_path, file_str)


def read_sigma_file(prefix, bath, pot):
    """ read the lennard-jones sigma file from its filesystem path
    """
    file_path = sigma_file_path(prefix, bath, pot)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.lennard_jones_sigma(file_str)
    return geo


def write_information_file(prefix, bath, pot, inf_obj):
    """ write the information file to its filesystem path
    """
    assert autoinf.matches_function_signature(inf_obj, information)
    file_path = information_file_path(prefix, bath, pot)
    file_str = autofile.write.information(inf_obj)
    autofile.write_file(file_path, file_str)


def read_information_file(prefix, bath, pot):
    """ read the information file from its filesystem path
    """
    file_path = information_file_path(prefix, bath, pot)
    file_str = autofile.read_file(file_path)
    inf_obj = autofile.read.information(file_str)
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj


# path definitions
BASE_DIR_NAME = 'LJ'


class BATHxGAS():
    """ bath gas """
    N2 = 'N2'
    HE = 'HE'
    NE = 'NE'
    AR = 'AR'
    KR = 'KR'


class POTENTIAL():
    """ lennard-jones pot """
    LJ126 = 'LJ126'
    BUCK = 'BUCK'
    REAL = 'REAL'


BATH_GASES = (BATHxGAS.N2, BATHxGAS.HE, BATHxGAS.NE, BATHxGAS.KR)
POTENTIALS = (POTENTIAL.LJ126, POTENTIAL.BUCK, POTENTIAL.REAL)


def directory_path(prefix, bath, pot):
    """ filesystem directory path
    """
    assert os.path.isdir(prefix)
    bath = str(bath).upper()
    pot = str(pot).upper()
    assert bath in BATH_GASES
    assert pot in POTENTIALS
    dir_names = (BASE_DIR_NAME, bath, pot)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def geometry_file_path(prefix, bath, pot):
    """ filesystem geometry file path
    """
    dir_path = directory_path(prefix, bath, pot)
    file_name = autofile.name.geometry(_FILExPREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def bath_geometry_file_path(prefix, bath, pot):
    """ filesystem geometry file path
    """
    dir_path = directory_path(prefix, bath, pot)
    file_name = autofile.name.geometry(_FILExPREFIX.BATH)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def epsilon_file_path(prefix, bath, pot):
    """ filesystem lennard-jones epsilon file path
    """
    dir_path = directory_path(prefix, bath, pot)
    file_name = autofile.name.lennard_jones_epsilon(_FILExPREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def sigma_file_path(prefix, bath, pot):
    """ filesystem lennard-jones sigma file path
    """
    dir_path = directory_path(prefix, bath, pot)
    file_name = autofile.name.lennard_jones_sigma(_FILExPREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def information_file_path(prefix, bath, pot):
    """ filesystem information file path
    """
    dir_path = directory_path(prefix, bath, pot)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return file_path


# information files
def information(nsamp):
    """ create an information object for lennard-jones information
    """
    assert isinstance(nsamp, numbers.Integral)
    inf_obj = autoinf.Info(nsamp=nsamp)
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj
