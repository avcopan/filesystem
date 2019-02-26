""" file readers
"""
import automol
import autoparse.find as apf


def energy(file_name):
    """ read an energy (hartree) from a file (hartree)
    """
    file_str = _read(file_name)
    assert apf.is_number(apf.strip_spaces(file_str))
    return float(file_str)


def geometry(file_name):
    """ read a geometry (bohr) from a file (angstrom)
    """
    file_str = _read(file_name)
    geo = automol.geom.from_xyz_string(file_str)
    return geo


def zmatrix(file_name):
    """ read a zmatrix (bohr/radian) from a file (angstrom/degree)
    """
    file_str = _read(file_name)
    zma = automol.zmatrix.from_zmat_string(file_str)
    return zma


def _read(file_name):
    with open(file_name, 'r') as file_obj:
        file_str = file_obj.read()
    return file_str
