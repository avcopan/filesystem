""" DataLayers
"""
import automol
import autodir.lib
from autodir import factory


class FilePrefix():
    """ file prefixes """
    INFO = 'info'


class DataFileAttributeName():
    """ DataFile attribute names """
    INFO = 'info'


# data layer generators
def species_trunk():
    """ species trunk DataLayer
    """
    ddir = autodir.lib.ddir.species_trunk()
    return factory.DataLayer(ddir=ddir)


def species_leaf():
    """ species leaf DataLayer
    """
    ddir = autodir.lib.ddir.species_leaf()
    inf_dfile = autodir.lib.dfile.information(
        ddir, FilePrefix.INFO, function=autodir.lib.info.species_leaf)

    # automatically write the information file when we create the directory
    def creation_side_effect_(prefix, args):
        ich, mult = args
        smi = automol.inchi.smiles(ich)
        inf_obj = autodir.lib.info.species_leaf(
            inchi=ich, smiles=smi, mult=mult)
        inf_dfile.write(inf_obj, prefix, args)
    ddir.creation_side_effect_ = creation_side_effect_

    dlayer = factory.DataLayer(
        ddir=ddir,
        dfiles={
            DataFileAttributeName.INFO: inf_dfile})
    return dlayer
