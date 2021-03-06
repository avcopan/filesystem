""" implements an class for YAML-style information
"""
from types import SimpleNamespace
try:
    from collections.abc import Sequence as _Sequence
except ImportError:
    from collections import Sequence as _Sequence
import yaml
from autoinf._inspect import function_keys as _function_keys


def object_(inf_dct):
    """ create an information object from a dictionary
    """
    inf_dct = {key: (object_(val) if isinstance(val, dict) else
                     (list(val) if _is_nonstring_sequence(val) else val))
               for key, val in inf_dct.items()}
    inf_obj = Info(**inf_dct)
    return inf_obj


def string(inf_obj):
    """ write an information object to a YAML string
    """
    inf_dct = dict(inf_obj)
    inf_str = yaml.dump(inf_dct, default_flow_style=False)
    return inf_str


def from_string(inf_str):
    """ read an information object from a YAML string
    """
    inf_dct = yaml.load(inf_str, Loader=yaml.FullLoader)
    inf_obj = object_(inf_dct)
    return inf_obj


def matches_function_signature(inf_obj, function):
    """ does the information object match this function signature?
    """
    assert isinstance(inf_obj, Info)
    return inf_obj.keys_() == _function_keys(function)


class Info(SimpleNamespace):
    """ information container class, implemented as a frozen namespace

    (values can change, but you can't add keys after initialization)
    """
    _frozen = False

    def _freeze(self):
        self._frozen = True

    def __init__(self, **kwargs):
        kwargs = {key: list(val) if _is_nonstring_sequence(val) else val
                  for key, val in kwargs.items()}
        super(Info, self).__init__(**kwargs)
        self._freeze()

    def keys_(self):
        """ keys for this instance """
        keys = frozenset(key for key in vars(self).keys()
                         if not key == '_frozen')
        return keys

    def _dict(self):
        keys = self.keys_()
        return {key: val for key, val in vars(self).items() if key in keys}

    def __iter__(self):
        """ used by the dict() function for conversion to dictionary """
        for key, val in self._dict().items():
            val = val if not isinstance(val, self.__class__) else dict(val)
            yield key, val

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        dct = self._dict()
        items = ("{}={!r}".format(k, dct[k]) for k in sorted(dct.keys()))
        return "Info({})".format(", ".join(items))

    def __setattr__(self, key, value):
        """ prevent adding new keys after the object is frozen """
        if self._frozen and not hasattr(self, key):
            raise TypeError("'{}' object does not support item assignment"
                            .format(self.__class__.__name__))
        object.__setattr__(self, key, value)


def _is_nonstring_sequence(obj):
    return (isinstance(obj, _Sequence)
            and not isinstance(obj, (str, bytes, bytearray)))
