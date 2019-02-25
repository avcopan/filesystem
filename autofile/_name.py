""" assign file names by type
"""
from .params import EXTENSION


def energy(file_name):
    """ adds energy extension, if missing
    """
    return _add_extension(file_name, EXTENSION.ENERGY)


def geometry(file_name):
    """ adds geometry extension, if missing
    """
    return _add_extension(file_name, EXTENSION.GEOMETRY)


def zmatrix(file_name):
    """ adds zmatrix extension, if missing
    """
    return _add_extension(file_name, EXTENSION.ZMATRIX)


def _add_extension(file_name, ext):
    if not str(file_name).endswith(ext):
        file_name = '{}{}'.format(file_name, ext)
    return file_name
