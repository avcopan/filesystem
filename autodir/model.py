""" defines the filesystem model for autodir
"""
import os
import glob
import autofile


class File():
    """ file I/O handler for a given datatype """

    def __init__(self, name, writer_=(lambda _: _), reader_=(lambda _: _)):
        """
        :param name: the file name
        :type name: str
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        """
        self.name = name
        self.writer_ = writer_
        self.reader_ = reader_

    def path(self, dir_path):
        """ file path
        """
        return os.path.join(dir_path, self.name)

    def exists(self, dir_path):
        """ does this file exist?
        """
        pth = self.path(dir_path)
        return os.path.isfile(pth)

    def write(self, val, dir_path):
        """ write data to a file
        """
        assert os.path.exists(dir_path)
        pth = self.path(dir_path)
        val_str = self.writer_(val)
        autofile.write_file(pth, val_str)

    def read(self, dir_path):
        """ read data from a file
        """
        assert self.exists(dir_path)
        pth = self.path(dir_path)
        val_str = self.reader_(pth)
        val = self.reader_(val_str)
        return val


class DataDir():
    """ directory creation manager """

    def __init__(self, map_, nspecs, depth, source_ddir=None):
        """
        :param map_: maps `nspecs` specifiers to a segment path consisting of
            `depth` directories
        """
        self.map_ = map_
        self.nspecs = nspecs
        self.depth = depth
        self.source = source_ddir

    def segment_path(self, specs=()):
        """ relative directory path
        """
        if self.source is None:
            assert len(specs) == self.nspecs
            spth = ''
        else:
            assert len(specs) >= self.nspecs
            sspecs = specs[:-self.nspecs]
            spth = self.source.segment_path(sspecs)
            specs = specs[-self.nspecs:]

        pth = self.map_(specs)
        assert _path_is_relative(pth)
        assert _path_has_depth(pth, self.depth)
        return os.path.join(spth, pth)

    def path(self, prefix, specs=()):
        """ absolute directory path
        """
        pfx = os.path.abspath(prefix)
        pth = self.segment_path(specs)
        return os.path.join(pfx, pth)

    def exists(self, prefix, specs=()):
        """ does this directory exist?
        """
        pth = self.path(prefix, specs)
        return os.path.isdir(pth)

    def create(self, prefix, specs=()):
        """ create a directory at this prefix
        """
        assert os.path.isdir(prefix)
        assert not self.exists(prefix, specs)
        dir_path = self.path(prefix, specs)
        os.makedirs(dir_path)

    def created_names(self, prefix, specs=()):
        """ names of the directories that have been created at this prefix
        """
        if self.source is None:
            pfx = prefix
        else:
            pfx = self.source.path(prefix, specs)

        assert os.path.isdir(pfx)
        cwd = os.getcwd()
        os.chdir(pfx)
        names = tuple(sorted(filter(
            os.path.isdir,
            glob.glob(os.path.join(*('*' * self.depth))))))
        os.chdir(cwd)
        return names


# helpers
def _path_is_relative(pth):
    """ is this a relative path?
    """
    return os.path.relpath(pth) == pth


def _path_has_depth(pth, depth):
    """ does this path have the given depth?
    """
    return len(_os_path_split_all(pth)) == depth


def _os_path_split_all(pth):
    """ grabbed this from the internet """
    allparts = []
    while 1:
        parts = os.path.split(pth)
        if parts[0] == pth:    # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == pth:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            pth = parts[0]
            allparts.insert(0, parts[1])
    return allparts


if __name__ == '__main__':
    import autodir.lib

    SPC_TRUNK_DDIR = DataDir(
        map_=(lambda x: autodir.lib.map_.species_trunk(*x)),
        nspecs=0,
        depth=1,
        source_ddir=None
    )

    SPC_LEAF_DDIR = DataDir(
        map_=(lambda x: autodir.lib.map_.species_leaf(*x)),
        nspecs=2,
        depth=4,
        source_ddir=SPC_TRUNK_DDIR,
    )

    THY_LEAF_DDIR = DataDir(
        map_=(lambda x: autodir.lib.map_.theory_leaf(*x)),
        nspecs=3,
        depth=1,
        source_ddir=SPC_LEAF_DDIR,
    )

    print(SPC_TRUNK_DDIR.path('.'))
    print(SPC_LEAF_DDIR.path('.', ['InChI=1S/O', 3]))

    SPECS = ['InChI=1S/O', 3, 'hf', 'sto-3g', False]
    if not THY_LEAF_DDIR.exists('.', SPECS):
        THY_LEAF_DDIR.create('.', SPECS)

    print()
    print(THY_LEAF_DDIR.created_names('.', SPECS[:2]))
