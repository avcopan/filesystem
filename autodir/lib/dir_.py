""" DataSeriesDirs
"""
try:
    from inspect import getfullargspec as function_argspec
except ImportError:
    from inspect import getargspec as function_argspec
from autodir import model
from autodir.lib import map_


def species_trunk():
    """ species trunk DataDir
    """
    _map = _pack_arguments(map_.species_trunk)
    nspecs = _count_arguments(map_.species_trunk)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1)


def species_leaf():
    """ species leaf DataDir
    """
    _map = _pack_arguments(map_.species_leaf)
    nspecs = _count_arguments(map_.species_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=4)


def theory_leaf():
    """ theory leaf DataDir
    """
    _map = _pack_arguments(map_.theory_leaf)
    nspecs = _count_arguments(map_.theory_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1)


def conformer_trunk():
    """ conformer trunk DataDir
    """
    _map = _pack_arguments(map_.conformer_trunk)
    nspecs = _count_arguments(map_.conformer_trunk)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1)


def conformer_leaf():
    """ conformer leaf DataDir
    """
    _map = _pack_arguments(map_.conformer_leaf)
    nspecs = _count_arguments(map_.conformer_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1)


# helpers
def _pack_arguments(function):
    """ generate an equivalent function that takes all of its arguments packed
    into a sequence
    """
    def _function(args=()):
        return function(*args)
    return _function


def _count_arguments(function):
    """ conut the number of arguments that a function takes in
    """
    argspec = function_argspec(function)
    return len(argspec.args)
