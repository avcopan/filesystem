""" string writers
"""
from numbers import Real as _Real
import yaml
import automol


def information(inf):
    """ write information (any dict/list combination) to a string
    """
    inf_str = yaml.dump(inf, default_flow_style=False)
    return inf_str


def energy(ene):
    """ write an energy (hartree) to a string (hartree)
    """
    ene_str = _float(ene)
    return ene_str


def geometry(geo):
    """ write a geometry (bohr) to a string (angstrom)
    """
    assert automol.geom.is_valid(geo)
    xyz_str = automol.geom.xyz_string(geo)
    return xyz_str


def zmatrix(zma):
    """ write a zmatrix (bohr/radian) to a string (angstroms/degree)
    """
    zma_str = automol.zmatrix.zmat_string(zma)
    return zma_str


def lennard_jones_epsilon(eps):
    """ write a lennard-jones epsilon (waveunmbers) to a string (wavenumbers)
    """
    eps_str = _float(eps)
    return eps_str


def lennard_jones_sigma(sig):
    """ write a lennard-jones sigma (angstrom) to a string (angstrom)
    """
    sig_str = _float(sig)
    return sig_str


def _float(val):
    assert isinstance(val, _Real)
    val_str = str(val)
    return val_str
