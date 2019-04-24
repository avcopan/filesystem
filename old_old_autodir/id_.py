""" string id generator and helpers
"""
import os
import base64
import autoparse.pattern as app
import autoparse.find as apf


def is_identifier(sid):
    """ is this a valid identifier?
    """
    sid_pattern = app.URLSAFE_CHAR * 12
    return apf.full_match(sid_pattern, sid)


def identifier():
    """ generate a "unique" (=long-ish, random) identifier
    """
    sid = base64.urlsafe_b64encode(os.urandom(9)).decode("utf-8")
    return sid


def directory_identifiers_at(dir_path):
    """ subdirectory names of this directory that are valid identifiers
    """
    assert os.path.isdir(dir_path)
    dir_names = next(os.walk(dir_path))[1]
    rids = tuple(filter(is_identifier, dir_names))
    return rids
