""" string readers
"""
import yaml
import automol
import autoparse.find as apf


def information(inf_str):
    """ read information (any dict/list combination) from a string
    """
    inf = yaml.load(inf_str)
    return inf


def energy(ene_str):
    """ read an energy (hartree) from a string (hartree)
    """
    ene = _float(ene_str)
    return ene


def geometry(xyz_str):
    """ read a geometry (bohr) from a string (angstrom)
    """
    geo = automol.geom.from_xyz_string(xyz_str)
    return geo


def zmatrix(zma_str):
    """ read a zmatrix (bohr/radian) from a string (angstrom/degree)
    """
    zma = automol.zmatrix.from_zmat_string(zma_str)
    return zma


def lennard_jones_epsilon(eps_str):
    """ read a lennard-jones epsilon (waveunmbers) from a string (wavenumbers)
    """
    eps = _float(eps_str)
    return eps


def lennard_jones_sigma(sig_str):
    """ read a lennard-jones sigma (angstrom) from a string (angstrom)
    """
    sig = _float(sig_str)
    return sig


def _float(val_str):
    assert apf.is_number(val_str)
    val = float(val_str)
    return val
