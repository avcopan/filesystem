""" connectivity filesystem
"""
import os
import numbers
import automol
import autofile
from autodir.params import FILExPREFIX as _FILExPREFIX


# filesystem create/read/write functions
def create(prefix, ich, mult):
    """ create this filesystem path
    """
    dir_path = directory_path(prefix, ich, mult)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    conn_inf = INFO.CONN.dict(ich=ich)
    inf = INFO.dict(ich=ich)
    _write_connectivity_information_file(prefix, ich, conn_inf)
    _write_information_file(prefix, ich, mult, inf)


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


def _write_connectivity_information_file(prefix, ich, inf):
    """ write the connectivity information file to its filesystem path

    (private because the user shouldn't be calling it)
    """
    file_path = _connectivity_information_file_path(prefix, ich)
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


def _connectivity_information_file_path(prefix, ich):
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
_ICH_KEY = 'inchi'
_SMI_KEY = 'smiles'


class INFO():
    """ information dictionaries """
    ICH_KEY = _ICH_KEY
    SMI_KEY = _SMI_KEY

    @classmethod
    def dict(cls, ich):
        """ inchi hash information dictionary
        """
        assert _is_valid_stereo_inchi(ich)
        smi = automol.inchi.smiles(ich)
        inf_dct = {cls.ICH_KEY: ich,
                   cls.SMI_KEY: smi}
        return inf_dct

    class CONN():
        """ inchi connectivity hash information """
        ICH_KEY = _ICH_KEY
        SMI_KEY = _SMI_KEY

        @classmethod
        def dict(cls, ich):
            """ inchi connectivity hash information dictionary
            """
            ich = automol.inchi.core_parent(ich)
            assert _is_valid_connectivity_inchi(ich)
            smi = automol.inchi.smiles(ich)
            inf_dct = {cls.ICH_KEY: ich,
                       cls.SMI_KEY: smi}
            return inf_dct
