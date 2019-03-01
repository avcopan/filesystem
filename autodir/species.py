""" species filesystem
"""
import os
import itertools
import autofile
import automol
from .params import PREFIX as _PREFIX

BASE_DIR_NAME = 'SPC'


class INFO():
    """ parameters for the information dictionary
    """
    ICH_KEY = 'inchi'
    SMI_KEY = 'smiles'


def schema(ich, mult):
    """ species directory schema

    :param ich: InChI string with complete stereo information
    :type ich: str
    :param mult: spin multiplicity (must be consistent with `ich`)
    :type mult: int
    :returns: a directory path and a dictionary of file strings by file path
    :rtype: (str, dict)
    """
    dir_names, inf_strs = zip(_base(),
                              _formula(ich),
                              _connectivity(ich),
                              _multiplicity(ich, mult),
                              _stereochemistry(ich))

    dir_path = os.path.join(*dir_names)

    inf_dir_paths = tuple(itertools.accumulate(dir_names, os.path.join))
    inf_paths = tuple(autofile.name.information(os.path.join(file_dir_path,
                                                             _PREFIX.INFO))
                      for file_dir_path in inf_dir_paths)

    file_spec_dct = {inf_path: inf_str
                     for inf_path, inf_str in zip(inf_paths, inf_strs)
                     if inf_str is not None}

    return dir_path, file_spec_dct


# directories
def _base():
    dir_name = BASE_DIR_NAME
    inf_str = None
    return (dir_name, inf_str)


def _formula(ich):
    dir_name = automol.inchi.formula_layer(ich)
    inf_str = None
    return (dir_name, inf_str)


def _connectivity(ich):
    ich = automol.inchi.core_parent(ich)
    assert automol.inchi.has_unknown_stereo_elements(ich) is True
    assert automol.inchi.is_closed(ich)
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    dir_name = automol.inchi.key.first_hash(ich_key)
    inf_str = _inchi_hash_information_string(ich)
    return (dir_name, inf_str)


def _multiplicity(ich, mult):
    assert mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))
    dir_name = '{:d}'.format(mult)
    inf_str = None
    return (dir_name, inf_str)


def _stereochemistry(ich):
    assert automol.inchi.has_unknown_stereo_elements(ich) is False
    assert automol.inchi.is_closed(ich)
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    dir_name = automol.inchi.key.second_hash(ich_key)
    inf_str = _inchi_hash_information_string(ich)
    return (dir_name, inf_str)


# helpers
def _inchi_hash_information_string(ich):
    smi = automol.inchi.smiles(ich)
    inf_dct = {
        INFO.ICH_KEY: ich,
        INFO.SMI_KEY: smi,
    }
    inf_str = autofile.write.information(inf_dct)
    return inf_str
