""" Info objects
"""
import numbers
import elstruct
import automol
import autoinf
from autodir.lib._util import is_valid_stereo_inchi as _is_valid_stereo_inchi


def species_leaf(inchi, smiles, mult):
    """ information for the species leaf directory
    """
    assert _is_valid_stereo_inchi(inchi)
    assert inchi == automol.smiles.inchi(smiles)
    inf_obj = autoinf.Info(inchi=inchi, smiles=smiles, mult=mult)
    assert autoinf.matches_function_signature(inf_obj, species_leaf)
    return inf_obj


def theory_leaf(method, basis, orb_restricted):
    """ information for the theory leaf directory

    This need not be tied to elstruct -- just take out the name checks.
    """
    assert elstruct.Method.contains(method)
    assert elstruct.Basis.contains(basis)
    assert isinstance(orb_restricted, bool)
    inf_obj = autoinf.Info(method=method, basis=basis,
                           orb_restricted=orb_restricted)
    assert autoinf.matches_function_signature(inf_obj, theory_leaf)
    return inf_obj


def conformer_trunk(nsamp, tors_info):
    """ information for the conformer trunk directory
    """
    tors_info = autoinf.Info(**dict(tors_info))
    assert isinstance(nsamp, numbers.Integral)
    inf_obj = autoinf.Info(nsamp=nsamp, tors_info=tors_info)
    assert autoinf.matches_function_signature(inf_obj, conformer_trunk)
    return inf_obj


def run(job, prog, method, basis, utc_start_time=None, utc_end_time=None):
    """ run information
    """
    inf_obj = autoinf.Info(
        job=job,
        prog=prog,
        method=method,
        basis=basis,
        utc_start_time=utc_start_time,
        utc_end_time=utc_end_time,
    )
    assert autoinf.matches_function_signature(inf_obj, run)
    return inf_obj
