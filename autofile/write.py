""" string writers
"""
from io import StringIO as _StringIO
from numbers import Real as _Real
import numpy
import automol
import autoinf


def information(inf_obj):
    """ write information (any dict/list combination) to a string
    """
    assert isinstance(inf_obj, autoinf.Info)
    inf_str = autoinf.string(inf_obj)
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


def trajectory(geo_lst, comments=None):
    """ write a series of geometries (bohr) to a string (angstrom)
    """
    assert all(map(automol.geom.is_valid, geo_lst))
    xyz_traj_str = automol.geom.xyz_trajectory_string(geo_lst,
                                                      comments=comments)
    return xyz_traj_str


def zmatrix(zma):
    """ write a zmatrix (bohr/radian) to a string (angstroms/degree)
    """
    assert automol.zmatrix.is_valid(zma)
    zma_str = automol.zmatrix.zmat_string(zma)
    return zma_str


def gradient(grad):
    """ write a gradient (hartree bohr^-1) to a string (hartree bohr^-1)
    """
    grad = numpy.array(grad)
    assert grad.ndim == 2 and grad.shape[1] == 3

    grad_str_io = _StringIO()
    numpy.savetxt(grad_str_io, grad)
    grad_str = grad_str_io.getvalue()
    grad_str_io.close()
    return grad_str


def hessian(hess):
    """ write a hessian (hartree bohr^-2) to a string (hartree bohr^-2)
    """
    hess = numpy.array(hess)
    assert hess.ndim == 2
    assert hess.shape[0] % 3 == 0 and hess.shape[0] == hess.shape[1]

    hess_str_io = _StringIO()
    numpy.savetxt(hess_str_io, hess)
    hess_str = hess_str_io.getvalue()
    hess_str_io.close()
    return hess_str


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
