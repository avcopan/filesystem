""" file namers
"""


class EXTENSION():
    """ file extensions """
    INFORMATION = '.yaml'
    ENERGY = '.ene'
    GEOMETRY = '.xyz'
    ZMATRIX = '.zmat'
    LJ_EPSILON = '.eps'
    LJ_SIGMA = '.sig'


def information(file_name):
    """ adds information extension, if missing
    """
    return _add_extension(file_name, EXTENSION.INFORMATION)


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
