""" DataSeriesDirs
"""
try:
    from inspect import getfullargspec as function_argspec
except ImportError:
    from inspect import getargspec as function_argspec
import automol
from autodir import model
from autodir.lib import map_
from autodir.lib import file_


SPEC_FILE_PREFIX = 'dir'


def species_trunk(source_dsdir=None):
    """ species trunk DataDir
    """
    _map = _pack_arguments(map_.species_trunk)
    nspecs = _count_arguments(map_.species_trunk)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1,
                               source_dsdir=source_dsdir)


def species_leaf(source_dsdir=None):
    """ species leaf DataDir
    """
    spec_dfile = file_.data_series_specifier(
        file_prefix=SPEC_FILE_PREFIX,
        map_dct_={
            'inchi': lambda specs: specs[0],
            'smiles': lambda specs: automol.inchi.smiles(specs[0]),
            'multiplicity': lambda specs: specs[1]},
        spec_keys=['inchi', 'multiplicity'])

    _map = _pack_arguments(map_.species_leaf)
    nspecs = _count_arguments(map_.species_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=4,
                               spec_dfile=spec_dfile,
                               source_dsdir=source_dsdir)


def theory_leaf(source_dsdir=None):
    """ theory leaf DataDir
    """
    spec_dfile = file_.data_series_specifier(
        file_prefix=SPEC_FILE_PREFIX,
        map_dct_={
            'method': lambda specs: specs[0],
            'basis': lambda specs: specs[1],
            'orb_restricted': lambda specs: specs[2]},
        spec_keys=['method', 'basis', 'orb_restricted'])

    _map = _pack_arguments(map_.theory_leaf)
    nspecs = _count_arguments(map_.theory_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1,
                               spec_dfile=spec_dfile,
                               source_dsdir=source_dsdir)


def conformer_trunk(source_dsdir=None):
    """ conformer trunk DataDir
    """
    _map = _pack_arguments(map_.conformer_trunk)
    nspecs = _count_arguments(map_.conformer_trunk)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1,
                               source_dsdir=source_dsdir)


def conformer_leaf(source_dsdir=None):
    """ conformer leaf DataDir
    """
    spec_dfile = file_.data_series_specifier(
        file_prefix=SPEC_FILE_PREFIX,
        map_dct_={'conformer_id': lambda specs: specs[0]},
        spec_keys=['conformer_id'])

    _map = _pack_arguments(map_.conformer_leaf)
    nspecs = _count_arguments(map_.conformer_leaf)
    return model.DataSeriesDir(map_=_map, nspecs=nspecs, depth=1,
                               spec_dfile=spec_dfile,
                               source_dsdir=source_dsdir)


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
