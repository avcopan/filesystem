""" species filesystem
"""
import os
import numbers
import functools
import automol
import autoinf
import autofile
from autodir import par
from autodir import util


# path definitions
BASE_DIR_NAME = 'SPC'


def conn_directory_path(prefix, ich):
    """ filesystem connectivity directory
    """
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)
    ich_fml = automol.inchi.formula_layer(ich)
    ich_hash1 = automol.inchi.key.first_hash(ich_key)
    dir_names = (BASE_DIR_NAME, ich_fml, ich_hash1)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


def directory_path(prefix, ich, mult):
    """ filesystem directory path
    """
    assert _is_valid_stereo_inchi(ich)
    assert isinstance(mult, numbers.Integral)
    assert mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))

    prefix = conn_directory_path(prefix, ich)

    ich_key = automol.inchi.inchi_key(ich)
    ich_hash2 = automol.inchi.key.second_hash(ich_key)
    mult_str = str(mult)
    dir_names = (mult_str, ich_hash2)
    dir_path = os.path.join(prefix, *dir_names)
    return dir_path


# filesystem create/read/write functions
def create(prefix, ich, mult):
    """ create this filesystem path
    """
    util.create_directory(
        prefix=prefix, dir_path=directory_path(prefix, ich, mult))

    smi = automol.inchi.smiles(ich)
    conn_ich = automol.inchi.core_parent(ich)
    conn_smi = automol.inchi.smiles(conn_ich)
    inf_obj = information(inchi=ich, smiles=smi)
    conn_inf_obj = conn_information(inchi=conn_ich, smiles=conn_smi)
    write_conn_information_file(prefix, ich, conn_inf_obj)
    write_information_file(prefix, ich, mult, inf_obj)


# conn information file
def conn_information(inchi, smiles):
    """ connectivity information object
    """
    assert _is_valid_connectivity_inchi(inchi)
    assert inchi == automol.smiles.inchi(smiles)
    inf_obj = autoinf.Info(inchi=inchi, smiles=smiles)
    assert autoinf.matches_function_signature(inf_obj, conn_information)
    return inf_obj


CONN_INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.INFO),
    dir_path_=conn_directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=conn_information),
)


def conn_information_file_path(prefix, ich):
    """ connectivity information file path
    """
    return CONN_INFORMATION_FILE.path([prefix, ich])


def has_conn_information_file(prefix, ich):
    """ does this filesystem have a connectivity information file?
    """
    return CONN_INFORMATION_FILE.exists([prefix, ich])


def write_conn_information_file(prefix, ich, conn_inf_obj):
    """ write the connectivity information file to its filesystem path
    """
    CONN_INFORMATION_FILE.write([prefix, ich], conn_inf_obj)


def read_conn_information_file(prefix, ich):
    """ read the connectivity information file from its filesystem path
    """
    return CONN_INFORMATION_FILE.read([prefix, ich])


# # information
def information(inchi, smiles):
    """ stereo information object
    """
    assert _is_valid_stereo_inchi(inchi)
    assert inchi == automol.smiles.inchi(smiles)
    inf_obj = autoinf.Info(inchi=inchi, smiles=smiles)
    assert autoinf.matches_function_signature(inf_obj, information)
    return inf_obj


INFORMATION_FILE = util.DataFile(
    file_name=autofile.name.information(par.FilePrefix.INFO),
    dir_path_=directory_path,
    writer_=autofile.write.information,
    reader_=autofile.read.information,
    checker_=functools.partial(
        autoinf.matches_function_signature, function=information),
)


def information_file_path(prefix, ich, mult):
    """ information file path
    """
    return INFORMATION_FILE.path([prefix, ich, mult])


def has_information_file(prefix, ich, mult):
    """ does this filesystem have an information file?
    """
    return INFORMATION_FILE.exists([prefix, ich, mult])


def write_information_file(prefix, ich, mult, inf_obj):
    """ write the information file to its filesystem path
    """
    INFORMATION_FILE.write([prefix, ich, mult], inf_obj)


def read_information_file(prefix, ich, mult):
    """ read the information file from its filesystem path
    """
    return INFORMATION_FILE.read([prefix, ich, mult])


# helper functions
def _is_valid_connectivity_inchi(ich):
    return (automol.inchi.is_closed(ich) and
            ich == automol.inchi.core_parent(ich))


def _is_valid_stereo_inchi(ich):
    return (automol.inchi.is_closed(ich) and
            automol.inchi.has_unknown_stereo_elements(ich) is False)
