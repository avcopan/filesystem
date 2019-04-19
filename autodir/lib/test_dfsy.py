""" test autodir.lib.dlayer
"""
import tempfile
from autodir.lib import dfsy

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species():
    """ tets dfsy.species
    """
    args_lst = [
        ('InChI=1S/O', 3),
        ('InChI=1S/O', 1),
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 1),
        ('InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1-', 1),
        ('InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-', 2),
    ]

    spc_fs = dfsy.species()

    for args in args_lst:
        assert not spc_fs.leaf.ddir.exists(PREFIX, args)
        assert not spc_fs.leaf.dfile.info.exists(PREFIX, args)
        spc_fs.leaf.ddir.create(PREFIX, args)
        assert spc_fs.leaf.ddir.exists(PREFIX, args)
        assert spc_fs.leaf.dfile.info.exists(PREFIX, args)

    print(spc_fs.leaf.ddir.created_names(PREFIX))
    # assert spc_fs.leaf.ddir.created_names(PREFIX) == (
    #     'C2H2F2/WFLOTYSKFUPZQB/1/OWOJBTED',
    #     'C2H2F2/WFLOTYSKFUPZQB/1/UPHRSURJ',
    #     'C5H5O/ZMKDIXNSHZUDML/2/ARJAWSKD',
    #     'O/QVGXLLKOCUKJST/1/UHFFFAOY',
    #     'O/QVGXLLKOCUKJST/3/UHFFFAOY',
    # )


if __name__ == '__main__':
    test__species()
