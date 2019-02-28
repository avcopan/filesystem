""" test the autodir module
"""
import os
import tempfile
import autodir

TMP_DIR = tempfile.mkdtemp()


def test__species():
    """ test species directory creation
    """
    ich = "InChI=1S/C5H5O/c1-2-3-4-5-6/h1-5H/b4-3-"
    mult = 2
    path_info = autodir.species.path_information(ich, mult)
    autodir.create_path(prefix=TMP_DIR, path_info=path_info)
    assert os.path.exists(os.path.join(TMP_DIR, path_info[0]))
    print(os.listdir(os.path.join(TMP_DIR, path_info[0])))


if __name__ == '__main__':
    test__species()
