""" conformer filesystem
"""
import os
import numbers
import autofile
from autodir.params import FILExPREFIX as _FILExPREFIX
from ._id import directory_identifier_names as _directory_identifier_names


# queries
def existing_identifiers(prefix):
    """ existing identifiers
    """
    dir_path = base_path(prefix)
    uids = (_directory_identifier_names(dir_path) if os.path.isdir(dir_path)
            else ())
    return uids


# filesystem create/read/write functions
def create_base(prefix):
    """ create the filesystem base path
    """
    dir_path = base_path(prefix)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def create(prefix, uid):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, uid)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def has_base_information_file(prefix):
    """ does this filesystem have a base information file?
    """
    file_path = base_information_file_path(prefix)
    return os.path.isfile(file_path)


def write_base_information_file(prefix, base_inf):
    """ write the base information file to its filesystem path
    """
    file_path = base_information_file_path(prefix)
    file_str = autofile.write.information(base_inf)
    autofile.write_file(file_path, file_str)


def read_base_information_file(prefix):
    """ read the base information file from its filesystem path
    """
    file_path = base_information_file_path(prefix)
    file_str = autofile.read_file(file_path)
    base_inf = autofile.read.information(file_str)
    return base_inf


def write_geometry_file(prefix, uid, geo):
    """ write the geometry file to its filesystem path
    """
    file_path = geometry_file_path(prefix, uid)
    file_str = autofile.write.geometry(geo)
    autofile.write_file(file_path, file_str)


def read_geometry_file(prefix, uid):
    """ read the geometry file from its filesystem path
    """
    file_path = geometry_file_path(prefix, uid)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.geometry(file_str)
    return geo


def write_energy_file(prefix, uid, geo):
    """ write the energy file to its filesystem path
    """
    file_path = energy_file_path(prefix, uid)
    file_str = autofile.write.energy(geo)
    autofile.write_file(file_path, file_str)


def read_energy_file(prefix, uid):
    """ read the energy file from its filesystem path
    """
    file_path = energy_file_path(prefix, uid)
    file_str = autofile.read_file(file_path)
    geo = autofile.read.energy(file_str)
    return geo


# path definitions
BASE_DIR_NAME = 'CONFS'


def base_path(prefix):
    """ base directory path
    """
    assert os.path.isdir(prefix)
    dir_names = (BASE_DIR_NAME,)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def base_information_file_path(prefix):
    """ base directory information file path
    """
    dir_path = base_path(prefix)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def directory_path(prefix, uid):
    """ conformer directory path
    """
    prefix = base_path(prefix)
    dir_path = os.path.join(prefix, uid)
    return dir_path


def geometry_file_path(prefix, uid):
    """ filesystem geometry file path
    """
    dir_path = directory_path(prefix, uid)
    file_name = autofile.name.geometry(_FILExPREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def energy_file_path(prefix, uid):
    """ filesystem energy file path
    """
    dir_path = directory_path(prefix, uid)
    file_name = autofile.name.energy(_FILExPREFIX.MAIN)
    file_path = os.path.join(dir_path, file_name)
    return file_path


# information files
class INFO():
    """ information dictionaries """

    class BASE():
        """ base information """
        NSAMP_KEY = 'nsamples'

        @classmethod
        def dict(cls, nsamp):
            """ base information dictionary
            """
            assert isinstance(nsamp, numbers.Integral)
            inf = {cls.NSAMP_KEY: nsamp}
            return inf
