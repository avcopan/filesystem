""" helper functions
"""
import os
import base64
import hashlib
import numbers
import automol
import autoparse.pattern as app
import autoparse.find as apf


def is_valid_stereo_inchi(ich):
    """ is this a valid inchi with complete stereo information?
    """
    return (automol.inchi.is_closed(ich) and
            automol.inchi.has_unknown_stereo_elements(ich) is False)


def is_valid_inchi_multiplicity(ich, mult):
    """ is this multiplicity compatible with this inchi string?
    """
    assert isinstance(mult, numbers.Integral)
    return mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))


def short_hash(string):
    """ determine a short (3-character) hash from a string
    """
    string = string.lower().encode('utf-8')
    dig = hashlib.md5(string).digest()
    hsh = base64.urlsafe_b64encode(dig)[:3]
    return hsh.decode()


def random_string_identifier():
    """ generate a "unique" (=long-ish, random) identifier
    """
    rsi = base64.urlsafe_b64encode(os.urandom(9)).decode("utf-8")
    return rsi


def is_random_string_identifier(sid):
    """ could this have been generated by `random_string_identifier()`?
    """
    sid_pattern = app.URLSAFE_CHAR * 12
    return apf.full_match(sid_pattern, sid)
