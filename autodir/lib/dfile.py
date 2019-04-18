""" DataFiles
"""
from autodir import factory
import autofile
import autoinf


def information(ddir, file_prefix, function=None):
    """ generate information DataFile
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

    file_name = autofile.name.information(file_prefix)
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def input_file(ddir, file_prefix):
    """ generate input file DataFile
    """
    file_name = autofile.name.input_file(file_prefix)
    return factory.DataFile(ddir=ddir, file_name=file_name)


def output_file(ddir, file_prefix):
    """ generate output file DataFile
    """
    file_name = autofile.name.output_file(file_prefix)
    return factory.DataFile(ddir=ddir, file_name=file_name)


def energy(ddir, file_prefix):
    """ generate energy DataFile
    """
    file_name = autofile.name.energy(file_prefix)
    writer_ = autofile.write.energy
    reader_ = autofile.read.energy
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def geometry(ddir, file_prefix):
    """ generate geometry DataFile
    """
    file_name = autofile.name.geometry(file_prefix)
    writer_ = autofile.write.geometry
    reader_ = autofile.read.geometry
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def gradient(ddir, file_prefix):
    """ generate gradient DataFile
    """
    file_name = autofile.name.gradient(file_prefix)
    writer_ = autofile.write.gradient
    reader_ = autofile.read.gradient
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def hessian(ddir, file_prefix):
    """ generate hessian DataFile
    """
    file_name = autofile.name.hessian(file_prefix)
    writer_ = autofile.write.hessian
    reader_ = autofile.read.hessian
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def zmatrix(ddir, file_prefix):
    """ generate zmatrix DataFile
    """
    file_name = autofile.name.zmatrix(file_prefix)
    writer_ = autofile.write.zmatrix
    reader_ = autofile.read.zmatrix
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def vmatrix(ddir, file_prefix):
    """ generate vmatrix DataFile
    """
    file_name = autofile.name.vmatrix(file_prefix)
    writer_ = autofile.write.vmatrix
    reader_ = autofile.read.vmatrix
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def trajectory(ddir, file_prefix):
    """ generate trajectory DataFile
    """
    file_name = autofile.name.trajectory(file_prefix)
    writer_ = autofile.write.trajectory
    reader_ = _not_implemented
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def lennard_jones_epsilon(ddir, file_prefix):
    """ generate lennard_jones_epsilon DataFile
    """
    file_name = autofile.name.lennard_jones_epsilon(file_prefix)
    writer_ = autofile.write.lennard_jones_epsilon
    reader_ = autofile.read.lennard_jones_epsilon
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


def lennard_jones_sigma(ddir, file_prefix):
    """ generate lennard_jones_sigma DataFile
    """
    file_name = autofile.name.lennard_jones_sigma(file_prefix)
    writer_ = autofile.write.lennard_jones_sigma
    reader_ = autofile.read.lennard_jones_sigma
    return factory.DataFile(ddir=ddir, file_name=file_name,
                            writer_=writer_, reader_=reader_)


# helpers
def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError
