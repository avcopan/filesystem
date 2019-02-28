""" species filesystem
"""
import os
import automol
from ._info import file_specs as _info_file_specs

BASE_DIR_NAME = 'SPC'


class INFO():
    """ parameters for the information dictionary
    """
    ICH_KEY = 'inchi'
    SMI_KEY = 'smiles'


def path_information(ich, mult):
    """ species path information

    :param ich: InChI string with complete stereo information
    :type ich: str
    :param mult: spin multiplicity (must be consistent with `ich`)
    :type mult: int
    """
    dir_names, info_dcts = zip(_base(),
                               _formula(ich),
                               _connectivity(ich),
                               _multiplicity(ich, mult),
                               _stereochemistry(ich))

    dir_path = os.path.join(*dir_names)
    file_spec_dct = _info_file_specs(dir_names, info_dcts)
    return dir_path, file_spec_dct


# directories
def _base():
    dir_name = BASE_DIR_NAME
    info_str = None
    return (dir_name, info_str)


def _formula(ich):
    dir_name = automol.inchi.formula_layer(ich)
    info_str = None
    return (dir_name, info_str)


def _connectivity(ich):
    ich = automol.inchi.core_parent(ich)
    assert automol.inchi.has_unknown_stereo_elements(ich) is True
    assert automol.inchi.is_closed(ich)
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    dir_name = automol.inchi.key.first_hash(ich_key)
    info_str = _inchi_hash_information(ich)
    return (dir_name, info_str)


def _multiplicity(ich, mult):
    assert mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))
    dir_name = '{:d}'.format(mult)
    info_str = None
    return (dir_name, info_str)


def _stereochemistry(ich):
    assert automol.inchi.has_unknown_stereo_elements(ich) is False
    assert automol.inchi.is_closed(ich)
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    dir_name = automol.inchi.key.second_hash(ich_key)
    info_str = _inchi_hash_information(ich)
    return (dir_name, info_str)


# helpers
def _inchi_hash_information(ich):
    smi = automol.inchi.smiles(ich)
    info_dct = {
        INFO.ICH_KEY: ich,
        INFO.SMI_KEY: smi,
    }
    return info_dct
