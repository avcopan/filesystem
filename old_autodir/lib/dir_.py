""" DataDirs
"""
try:
    from inspect import getfullargspec as function_argspec
except ImportError:
    from inspect import getargspec as function_argspec
from autodir import factory
from autodir.lib import name


def species_trunk():
    """ species trunk DataDir
    """
    name_ = _pack_arguments(name.species_trunk)
    nargs = _count_arguments(name.species_trunk)
    return factory.DataDir(name_=name_, nargs=nargs, depth=1)


def species_leaf():
    """ species leaf DataDir
    """
    name_ = _pack_arguments(name.species_leaf)
    nargs = _count_arguments(name.species_leaf)
    return factory.DataDir(name_=name_, nargs=nargs, depth=4)


def theory_leaf():
    """ theory leaf DataDir
    """
    name_ = _pack_arguments(name.theory_leaf)
    nargs = _count_arguments(name.theory_leaf)
    return factory.DataDir(name_=name_, nargs=nargs, depth=1)


def conformer_trunk():
    """ conformer trunk DataDir
    """
    name_ = _pack_arguments(name.conformer_trunk)
    nargs = _count_arguments(name.conformer_trunk)
    return factory.DataDir(name_=name_, nargs=nargs, depth=1)


def conformer_leaf():
    """ conformer leaf DataDir
    """
    name_ = _pack_arguments(name.conformer_leaf)
    nargs = _count_arguments(name.conformer_leaf)
    return factory.DataDir(name_=name_, nargs=nargs, depth=1)


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
