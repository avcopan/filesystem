""" uuid helpers
"""
import os
import uuid


def unique_identifier():
    """ generate a unique identifier
    """
    return str(uuid.uuid4()).upper()


def directory_identifier_names(dir_path):
    """ list the directory names that are identifiers at a given path
    """
    assert os.path.isdir(dir_path)
    dir_names = next(os.walk(dir_path))[1]
    uids = tuple(filter(is_identifier, dir_names))
    return uids


def is_identifier(obj, version=4):
    """ is this a uid?
    """
    try:
        ret = True
        uuid.UUID(obj, version=version)
    except (ValueError, AttributeError):
        ret = False

    return ret
