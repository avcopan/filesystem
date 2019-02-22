""" file writers
"""
from numbers import Real as _Real
import automol
from .params import EXTENSION


def energy(file_name, ene):
    """ write an energy in hartrees to a file in hartrees
    """
    file_name = _add_extension(file_name, EXTENSION.ENERGY)
    assert isinstance(ene, _Real)
    ene_str = str(ene)
    _write(file_name, ene_str)


def geometry(file_name, geo):
    """ write a geometry in bohr to a file in angstroms
    """
    file_name = _add_extension(file_name, EXTENSION.GEOMETRY)
    assert automol.geom.is_valid(geo)
    xyz_str = automol.geom.xyz_string(geo)
    _write(file_name, xyz_str)


def zmatrix(file_name, zma, var_dct=None):
    """ write a zmatrix in bohr/radians to a file in angstroms/degrees
    """
    file_name = _add_extension(file_name, EXTENSION.ZMATRIX)
    zma_str = automol.zmatrix.zmat_string(zma, var_dct=var_dct)
    _write(file_name, zma_str)


def _add_extension(file_name, ext):
    if not str(file_name).endswith(ext):
        file_name = '{}{}'.format(file_name, ext)
    return file_name


def _write(file_name, string):
    with open(file_name, 'w') as file_obj:
        file_obj.write(string)
