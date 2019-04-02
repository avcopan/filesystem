""" file namers
"""


class EXTENSION():
    """ file extensions """
    INFORMATION = '.yaml'
    INPUT_LOG = '.inp'
    OUTPUT_LOG = '.out'
    SHELL_SCRIPT = '.sh'
    ENERGY = '.ene'
    GEOMETRY = '.xyz'
    ZMATRIX = '.zmat'
    GRADIENT = '.grad'
    HESSIAN = '.hess'
    LJ_EPSILON = '.eps'
    LJ_SIGMA = '.sig'


def information(file_name):
    """ adds information extension, if missing
    """
    return _add_extension(file_name, EXTENSION.INFORMATION)


def input_file(file_name):
    """ adds input file extension, if missing
    """
    return _add_extension(file_name, EXTENSION.INPUT_LOG)


def output_file(file_name):
    """ adds output file extension, if missing
    """
    return _add_extension(file_name, EXTENSION.OUTPUT_LOG)


def run_script(file_name):
    """ adds run script extension, if missing
    """
    return _add_extension(file_name, EXTENSION.SHELL_SCRIPT)


def energy(file_name):
    """ adds energy extension, if missing
    """
    return _add_extension(file_name, EXTENSION.ENERGY)


def geometry(file_name):
    """ adds geometry extension, if missing
    """
    return _add_extension(file_name, EXTENSION.GEOMETRY)


def zmatrix(file_name):
    """ adds zmatrix extension, if missing
    """
    return _add_extension(file_name, EXTENSION.ZMATRIX)


def gradient(file_name):
    """ adds gradient extension, if missing
    """
    return _add_extension(file_name, EXTENSION.GRADIENT)


def hessian(file_name):
    """ adds hessian extension, if missing
    """
    return _add_extension(file_name, EXTENSION.HESSIAN)


def lennard_jones_epsilon(file_name):
    """ adds lennard-jones epsilon extension, if missing
    """
    return _add_extension(file_name, EXTENSION.LJ_EPSILON)


def lennard_jones_sigma(file_name):
    """ adds lennard-jones sigma extension, if missing
    """
    return _add_extension(file_name, EXTENSION.LJ_SIGMA)


def _add_extension(file_name, ext):
    if not str(file_name).endswith(ext):
        file_name = '{}{}'.format(file_name, ext)
    return file_name
