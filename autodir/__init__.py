""" defines standard directory paths for quantum chemistry data
"""
from . import schema
# schemata
from . import species
from . import theory
from . import lj

__all__ = [
    'schema',
    # schemata
    'species',
    'theory',
    'lj',
]
