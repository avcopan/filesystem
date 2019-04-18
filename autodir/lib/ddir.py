""" DataDirs
"""
try:
    from inspect import getfullargspec as function_argspec
except ImportError:
    from inspect import getargspec as function_argspec
from autodir import factory
from autodir.lib import dname


def species_trunk():
    """ species trunk DataDir
    """
    name_ = _pack_arguments(dname.species_trunk)
    nargs = _count_arguments(dname.species_trunk)
    return factory.DataDir(name_=name_, nargs=nargs)


def species_leaf():
    """ species trunk DataDir
    """
    name_ = _pack_arguments(dname.species_leaf)
    nargs = _count_arguments(dname.species_leaf)
    return factory.DataDir(name_=name_, nargs=nargs)


def theory_leaf():
    """ theory leaf DataDir
    """
    name_ = _pack_arguments(dname.theory_leaf)
    nargs = _count_arguments(dname.theory_leaf)
    return factory.DataDir(name_=name_, nargs=nargs)


def conformer_trunk():
    """ conformer trunk DataDir
    """
    name_ = _pack_arguments(dname.conformer_trunk)
    nargs = _count_arguments(dname.conformer_trunk)
    return factory.DataDir(name_=name_, nargs=nargs)


def conformer_leaf():
    """ conformer trunk DataDir
    """
    name_ = _pack_arguments(dname.conformer_leaf)
    nargs = _count_arguments(dname.conformer_leaf)
    return factory.DataDir(name_=name_, nargs=nargs)


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
