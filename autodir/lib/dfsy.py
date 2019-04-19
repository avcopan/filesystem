""" DataFileSystems
"""
import autodir.lib
from autodir import factory


class DataLayerAttributeName():
    """ DataLayer attribute names """
    TRUNK = 'trunk'
    LEAF = 'leaf'


def species():
    """ species DataFileSystem
    """
    trunk_dlayer = autodir.lib.dlayer.species_trunk()
    leaf_dlayer = autodir.lib.dlayer.species_leaf()
    return factory.DataFileSystem(
        [(DataLayerAttributeName.TRUNK, trunk_dlayer),
         (DataLayerAttributeName.LEAF, leaf_dlayer)])
