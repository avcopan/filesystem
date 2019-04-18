""" directory naming functions
"""
import os
import numbers
import base64
import hashlib
import automol
import elstruct
import autoparse.pattern as app
import autoparse.find as apf


# species
def species_trunk():
    """ species trunk directory name
    """
    return 'SPC'


def species_leaf(ich, mult):
    """ species leaf directory name
    """
    assert isinstance(mult, numbers.Integral)
    assert mult in automol.graph.possible_spin_multiplicities(
        automol.inchi.connectivity_graph(ich))
    ich_key = automol.inchi.inchi_key(ich)
    assert automol.inchi.key.is_standard_neutral(ich_key)

    mult_str = '{:d}'.format(mult)
    dir_names = (automol.inchi.formula_layer(ich),
                 automol.inchi.key.first_hash(ich_key),
                 mult_str,
                 automol.inchi.key.second_hash(ich_key),)
    return os.path.join(*dir_names)


def _is_valid_stereo_inchi(ich):
    return (automol.inchi.is_closed(ich) and
            automol.inchi.has_unknown_stereo_elements(ich) is False)


# theory
def theory_leaf(method, basis, orb_restricted):
    """ theory leaf directory name

    This need not be tied to elstruct -- just take out the name checks.
    Note that we are (no longer) checking the orbital restriction.
    """
    assert elstruct.Method.contains(method)
    assert elstruct.Basis.contains(basis)
    assert isinstance(orb_restricted, bool)

    ref_char = 'R' if orb_restricted else 'U'
    dir_name = ''.join([_short_hash(method),
                        _short_hash(basis),
                        ref_char])
    return dir_name


def _short_hash(string):
    """ determine a short (3-character) hash from a string
    """
    string = string.lower().encode('utf-8')
    dig = hashlib.md5(string).digest()
    hsh = base64.urlsafe_b64encode(dig)[:3]
    return hsh.decode()


# conformer
def conformer_trunk():
    """ conformer trunk directory name
    """
    return 'CONFS'


def conformer_leaf(cid):
    """ conformer leaf directory name
    """
    assert _is_conformer_id(cid)
    return cid


def new_conformer_id():
    """ generate a "unique" (=long-ish, random) identifier
    """
    cid = base64.urlsafe_b64encode(os.urandom(9)).decode("utf-8")
    return cid


def _is_conformer_id(sid):
    """ is this a valid identifier?
    """
    sid_pattern = app.URLSAFE_CHAR * 12
    return apf.full_match(sid_pattern, sid)
