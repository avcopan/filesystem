""" defines standard directory paths for quantum chemistry data
"""
from autodir import theory
from autodir import species
from autodir import conf
from autodir import lj
# functions
from ._id import unique_identifier


__all__ = [
    'species',
    'theory',
    'conf',
    'lj',
    'unique_identifier',
]
