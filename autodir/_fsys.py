""" DataFileSystems
"""
import autodir.lib
from autodir import factory


class DataLayerAttributeName():
    """ DataLayer attribute names """
    SPECIES_TRUNK = 'species_trunk'
    SPECIES_LEAF = 'species'
    THEORY_LEAF = 'theory'
    CONFORMER_TRUNK = 'conformer_trunk'
    CONFORMER_LEAF = 'conformer'


def filesystem():
    """ creates the entire FileSystem object by stacking and merging DataLayers
    """
    fs_ = factory.FileSystem.by_stacking([
        (DataLayerAttributeName.SPECIES_TRUNK,
         autodir.lib.layer.species_trunk()),
        (DataLayerAttributeName.SPECIES_LEAF,
         autodir.lib.layer.species_leaf()),
        (DataLayerAttributeName.THEORY_LEAF,
         autodir.lib.layer.theory_leaf()),
        (DataLayerAttributeName.CONFORMER_TRUNK,
         autodir.lib.layer.conformer_trunk()),
        (DataLayerAttributeName.CONFORMER_LEAF,
         autodir.lib.layer.conformer_leaf())])
    return fs_
