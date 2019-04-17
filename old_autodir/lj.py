""" lennard-jones filesystem
"""
import os
import numbers
import functools
import autoinf
import autofile
from autodir import par
from autodir import util


class BathGas():
    """ bath gas """
    N2 = 'N2'
    HE = 'HE'
    NE = 'NE'
    AR = 'AR'
    KR = 'KR'


class Potential():
    """ lennard-jones potential """
    LJ126 = 'LJ126'
    BUCK = 'BUCK'
    REAL = 'REAL'


BATH_GASES = (BathGas.N2, BathGas.HE, BathGas.NE, BathGas.KR)
POTENTIALS = (Potential.LJ126, Potential.BUCK, Potential.REAL)


# path definitions
BASE_DIR_NAME = 'LJ'


def directory_path(prefix, bath, pot):
    """ filesystem directory path
    """
    bath = str(bath).upper()
    pot = str(pot).upper()
    assert bath in BATH_GASES
    assert pot in POTENTIALS
    dir_names = (BASE_DIR_NAME, bath, pot)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


# filesystem create/read/write functions
def create(prefix, bath, pot):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix, dir_path=directory_path(prefix, bath, pot))


# # information file
def information(nsamp):
    """ create an information object for lennard-jones information
    """
    assert isinstance(nsamp, numbers.Integral)
    inf_obj = autoinf.Info(nsamp=nsamp)
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj


INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.LJ),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=information),
)


def information_file_path(prefix, bath, pot):
    """ gradient information file path
    """
    return INFORMATION_FILE.path([prefix, bath, pot])


def has_information_file(prefix, bath, pot):
    """ does this filesystem have a gradient information file?
    """
    return INFORMATION_FILE.exists([prefix, bath, pot])


def write_information_file(prefix, bath, pot, grad_inp_str):
    """ write the gradient information file to its filesystem path
    """
    INFORMATION_FILE.write([prefix, bath, pot], grad_inp_str)


def read_information_file(prefix, bath, pot):
    """ read the gradient information file from its filesystem path
    """
    return INFORMATION_FILE.read([prefix, bath, pot])


# # geometry file
GEOMETRY_FILE = util.DataFile(
    file_name=autofile.name.geometry(par.FilePrefix.LJ),
    dir_path_=directory_path,
    writer_=autofile.write.geometry,
    reader_=autofile.read.geometry,
)


def geometry_file_path(prefix, bath, pot):
    """ geometry file path
    """
    return GEOMETRY_FILE.path([prefix, bath, pot])


def has_geometry_file(prefix, bath, pot):
    """ does this filesystem have a geometry file?
    """
    return GEOMETRY_FILE.exists([prefix, bath, pot])


def write_geometry_file(prefix, bath, pot, geo):
    """ write the geometry file to its filesystem path
    """
    GEOMETRY_FILE.write([prefix, bath, pot], geo)


def read_geometry_file(prefix, bath, pot):
    """ read the geometry file from its filesystem path
    """
    return GEOMETRY_FILE.read([prefix, bath, pot])


# # bath geometry file
BATH_GEOMETRY_FILE = util.DataFile(
    file_name=autofile.name.geometry(par.FilePrefix.BATH),
    dir_path_=directory_path,
    writer_=autofile.write.geometry,
    reader_=autofile.read.geometry,
)


def bath_geometry_file_path(prefix, bath, pot):
    """ bath geometry file path
    """
    return BATH_GEOMETRY_FILE.path([prefix, bath, pot])


def has_bath_geometry_file(prefix, bath, pot):
    """ does this filesystem have a bath geometry file?
    """
    return BATH_GEOMETRY_FILE.exists([prefix, bath, pot])


def write_bath_geometry_file(prefix, bath, pot, geo):
    """ write the bath geometry file to its filesystem path
    """
    BATH_GEOMETRY_FILE.write([prefix, bath, pot], geo)


def read_bath_geometry_file(prefix, bath, pot):
    """ read the bath geometry file from its filesystem path
    """
    return BATH_GEOMETRY_FILE.read([prefix, bath, pot])


# # epsilon file
EPSILON_FILE = util.DataFile(
    file_name=autofile.name.lennard_jones_epsilon(par.FilePrefix.LJ),
    dir_path_=directory_path,
    writer_=autofile.write.lennard_jones_epsilon,
    reader_=autofile.read.lennard_jones_epsilon,
)


def epsilon_file_path(prefix, bath, pot):
    """ epsilon file path
    """
    return EPSILON_FILE.path([prefix, bath, pot])


def has_epsilon_file(prefix, bath, pot):
    """ does this filesystem have a epsilon file?
    """
    return EPSILON_FILE.exists([prefix, bath, pot])


def write_epsilon_file(prefix, bath, pot, geo):
    """ write the epsilon file to its filesystem path
    """
    EPSILON_FILE.write([prefix, bath, pot], geo)


def read_epsilon_file(prefix, bath, pot):
    """ read the epsilon file from its filesystem path
    """
    return EPSILON_FILE.read([prefix, bath, pot])


# # sigma file
SIGMA_FILE = util.DataFile(
    file_name=autofile.name.lennard_jones_sigma(par.FilePrefix.LJ),
    dir_path_=directory_path,
    writer_=autofile.write.lennard_jones_sigma,
    reader_=autofile.read.lennard_jones_sigma,
)


def sigma_file_path(prefix, bath, pot):
    """ sigma file path
    """
    return SIGMA_FILE.path([prefix, bath, pot])


def has_sigma_file(prefix, bath, pot):
    """ does this filesystem have a sigma file?
    """
    return SIGMA_FILE.exists([prefix, bath, pot])


def write_sigma_file(prefix, bath, pot, geo):
    """ write the sigma file to its filesystem path
    """
    SIGMA_FILE.write([prefix, bath, pot], geo)


def read_sigma_file(prefix, bath, pot):
    """ read the sigma file from its filesystem path
    """
    return SIGMA_FILE.read([prefix, bath, pot])
