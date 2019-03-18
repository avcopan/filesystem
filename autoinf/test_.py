""" test the autoinf module
"""
import autoinf


def test_():
    """ tests
    """
    inf_obj = autoinf.Info(a=['b', 'c', 'd', 'e'], x=autoinf.Info(y=1, z=2))
    assert dict(inf_obj) == {'a': ['b', 'c', 'd', 'e'], 'x': {'y': 1, 'z': 2}}
    assert autoinf.object_(dict(inf_obj)) == inf_obj
