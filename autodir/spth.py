""" a convenience module for species/theory filesystems
"""
from autodir import species
from autodir import theory


# path definitions
def directory_path(prefix, ich, mult, method, basis, open_shell,
                   orb_restricted):
    """ species/theory directory path
    """
    return theory.directory_path(
        prefix=species.directory_path(prefix, ich, mult),
        method=method, basis=basis, open_shell=open_shell,
        orb_restricted=orb_restricted)


# filesystem create/read/write functions
def create(prefix, ich, mult, method, basis, open_shell, orb_restricted):
    """ create species/theory filesystem path
    """
    species.create(prefix, ich, mult)
    theory.create(
        prefix=species.directory_path(prefix, ich, mult),
        method=method, basis=basis, open_shell=open_shell,
        orb_restricted=orb_restricted)
