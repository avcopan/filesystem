""" file writers
"""
from numbers import Real as _Real
import automol
from ._name import energy as _energy_file_name
from ._name import geometry as _geometry_file_name
from ._name import zmatrix as _zmatrix_file_name


def energy(file_name, ene):
    """ write an energy (hartree) to a file (hartree)
    """
    assert file_name == _energy_file_name(file_name)
    assert isinstance(ene, _Real)
    ene_str = str(ene)
    _write(file_name, ene_str)


def geometry(file_name, geo):
    """ write a geometry (bohr) to a file (angstrom)
    """
    assert file_name == _geometry_file_name(file_name)
    assert automol.geom.is_valid(geo)
    xyz_str = automol.geom.xyz_string(geo)
    _write(file_name, xyz_str)


def zmatrix(file_name, zma, var_dct=None):
    """ write a zmatrix (bohr/radian) to a file (angstroms/degree)
    """
    assert file_name == _zmatrix_file_name(file_name)
    zma_str = automol.zmatrix.zmat_string(zma, var_dct=var_dct)
    _write(file_name, zma_str)


def _write(file_name, string):
    with open(file_name, 'w') as file_obj:
        file_obj.write(string)
