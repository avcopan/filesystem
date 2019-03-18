""" connectivity filesystem
"""
import os
import numbers
import automol
import autoinf
import autofile
from autodir.params import FILExPREFIX as _FILExPREFIX


# filesystem create/read/write functions
def create(prefix, ich, mult):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, ich, mult)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    smi = automol.inchi.smiles(ich)
    conn_ich = automol.inchi.core_parent(ich)
    conn_smi = automol.inchi.smiles(conn_ich)
    inf_obj = hash_information(inchi=ich, smiles=smi)
    conn_inf_obj = connectivity_hash_information(inchi=conn_ich,
                                                 smiles=conn_smi)
    _write_connectivity_hash_information_file(prefix, ich, conn_inf_obj)
    _write_information_file(prefix, ich, mult, inf_obj)


def read_information_file(prefix, ich, mult):
    """ read the information file from its filesystem path
    """
    file_path = information_file_path(prefix, ich, mult)
    file_str = autofile.read_file(file_path)
    inf = autofile.read.information(file_str)
    return inf


def _write_information_file(prefix, ich, mult, inf):
    """ write the information file to its filesystem path

    (private because the user shouldn't be calling it)
    """
    file_path = information_file_path(prefix, ich, mult)
    file_str = autofile.write.information(inf)
    autofile.write_file(file_path, file_str)


def _write_connectivity_hash_information_file(prefix, ich, inf):
    """ write the connectivity information file to its filesystem path

    (private because the user shouldn't be calling it)
    """
    file_path = _connectivity_hash_information_file_path(prefix, ich)
    file_str = autofile.write.information(inf)
    autofile.write_file(file_path, file_str)


# path definitions
BASE_DIR_NAME = 'SPC'


def directory_path(prefix, ich, mult):
    """ filesystem directory path
    """
    assert _is_valid_stereo_inchi(ich)
    assert isinstance(mult, numbers.Integral)
    assert mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))

    prefix = _connectivity_directory_path(prefix, ich)

    ich_key = automol.inchi.inchi_key(ich)
    ich_hash2 = automol.inchi.key.second_hash(ich_key)
    mult_str = str(mult)
    dir_names = (mult_str, ich_hash2)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def information_file_path(prefix, ich, mult):
    """ filesystem information file path
    """
    dir_path = directory_path(prefix, ich, mult)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def _connectivity_directory_path(prefix, ich):
    """ filesystem connectivity directory
    """
    assert os.path.isdir(prefix)
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    ich_fml = automol.inchi.formula_layer(ich)
    ich_hash1 = automol.inchi.key.first_hash(ich_key)
    dir_names = (BASE_DIR_NAME, ich_fml, ich_hash1)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def _connectivity_hash_information_file_path(prefix, ich):
    """ filesystem information file path
    """
    dir_path = _connectivity_directory_path(prefix, ich)
    file_name = autofile.name.information(_FILExPREFIX.INFO)
    file_path = os.path.join(dir_path, file_name)
    return file_path


# helper functions
def _is_valid_connectivity_inchi(ich):
    return (automol.inchi.is_closed(ich) and
            ich == automol.inchi.core_parent(ich))


def _is_valid_stereo_inchi(ich):
    return (automol.inchi.is_closed(ich) and
            automol.inchi.has_unknown_stereo_elements(ich) is False)


# information files
def hash_information(inchi, smiles):
    """ stereo information object
    """
    assert _is_valid_stereo_inchi(inchi)
    assert inchi == automol.smiles.inchi(smiles)
    inf_obj = autoinf.Info(inchi=inchi, smiles=smiles)
    assert autoinf.matches_function_signature(inf_obj, hash_information)
    return inf_obj


def connectivity_hash_information(inchi, smiles):
    """ connectivity information object
    """
    assert _is_valid_connectivity_inchi(inchi)
    assert inchi == automol.smiles.inchi(smiles)
    inf_obj = autoinf.Info(inchi=inchi, smiles=smiles)
    assert autoinf.matches_function_signature(inf_obj,
                                              connectivity_hash_information)
    return inf_obj
