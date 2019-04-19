""" Info objects
"""
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
