""" DataFiles
"""
from autodir import model
import autofile
import autoinf


def information(file_prefix, function=None):
    """ information DataFile

    :param function: optional information-generator function, for checking the
        function signature against the information object
    :type function: callable
    """
    def writer_(inf_obj):
        if function is not None:
            assert autoinf.matches_function_signature(inf_obj, function)
        inf_str = autofile.write.information(inf_obj)
        return inf_str

    def reader_(inf_str):
        inf_obj = autofile.read.information(inf_str)
        if function is not None:
            assert autoinf.matches_function_signature(inf_obj, function)
        return inf_obj

    name = autofile.name.information(file_prefix)
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def data_series_specifier(file_prefix, map_dct_, spec_keys):
    """ data series specifier DataFile

    Specifiers are stored in information files according to `map_dct_` and read
    back out according to `spec_keys_`. The file may contain auxiliary
    information (such as SMILES along with InChI), but for the read to work it
    must contain each specifier value.

    :param map_dct_: Maps on the specifier list to the values stored in the
        information file, by key.
    :type map_dct_: dict[key: callable]
    :param spec_keys: Keys to the original specifier values.
    :type spec_keys: tuple[str]
    """

    def writer_(specs):
        inf_dct = {key: map_(specs) for key, map_ in map_dct_.items()}
        inf_obj = autoinf.object_(inf_dct)
        return autofile.write.information(inf_obj)

    def reader_(inf_str):
        inf_obj = autofile.read.information(inf_str)
        inf_dct = dict(inf_obj)
        return tuple(map(inf_dct.__getitem__, spec_keys))

    name = autofile.name.information(file_prefix)
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def input_file(file_prefix):
    """ generate input file DataFile
    """
    name = autofile.name.input_file(file_prefix)
    return model.DataFile(name=name)


def output_file(file_prefix):
    """ generate output file DataFile
    """
    name = autofile.name.output_file(file_prefix)
    return model.DataFile(name=name)


def energy(file_prefix):
    """ generate energy DataFile
    """
    name = autofile.name.energy(file_prefix)
    writer_ = autofile.write.energy
    reader_ = autofile.read.energy
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def geometry(file_prefix):
    """ generate geometry DataFile
    """
    name = autofile.name.geometry(file_prefix)
    writer_ = autofile.write.geometry
    reader_ = autofile.read.geometry
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def gradient(file_prefix):
    """ generate gradient DataFile
    """
    name = autofile.name.gradient(file_prefix)
    writer_ = autofile.write.gradient
    reader_ = autofile.read.gradient
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def hessian(file_prefix):
    """ generate hessian DataFile
    """
    name = autofile.name.hessian(file_prefix)
    writer_ = autofile.write.hessian
    reader_ = autofile.read.hessian
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def zmatrix(file_prefix):
    """ generate zmatrix DataFile
    """
    name = autofile.name.zmatrix(file_prefix)
    writer_ = autofile.write.zmatrix
    reader_ = autofile.read.zmatrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def vmatrix(file_prefix):
    """ generate vmatrix DataFile
    """
    name = autofile.name.vmatrix(file_prefix)
    writer_ = autofile.write.vmatrix
    reader_ = autofile.read.vmatrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def trajectory(file_prefix):
    """ generate trajectory DataFile
    """
    name = autofile.name.trajectory(file_prefix)
    writer_ = autofile.write.trajectory
    reader_ = _not_implemented
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def lennard_jones_epsilon(file_prefix):
    """ generate lennard_jones_epsilon DataFile
    """
    name = autofile.name.lennard_jones_epsilon(file_prefix)
    writer_ = autofile.write.lennard_jones_epsilon
    reader_ = autofile.read.lennard_jones_epsilon
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def lennard_jones_sigma(file_prefix):
    """ generate lennard_jones_sigma DataFile
    """
    name = autofile.name.lennard_jones_sigma(file_prefix)
    writer_ = autofile.write.lennard_jones_sigma
    reader_ = autofile.read.lennard_jones_sigma
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


# helpers
def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError
