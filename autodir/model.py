""" defines the filesystem model for autodir
"""
import os
import glob
import autoinf
import autofile


class DataFile():
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

    def path(self, dir_pth):
        """ file path
        """
        return os.path.join(dir_pth, self.name)

    def exists(self, dir_pth):
        """ does this file exist?
        """
        pth = self.path(dir_pth)
        return os.path.isfile(pth)

    def write(self, val, dir_pth):
        """ write data to this file
        """
        assert os.path.exists(dir_pth)
        pth = self.path(dir_pth)
        val_str = self.writer_(val)
        autofile.write_file(pth, val_str)

    def read(self, dir_pth):
        """ read data from this file
        """
        assert self.exists(dir_pth)
        pth = self.path(dir_pth)
        val_str = autofile.read_file(pth)
        val = self.reader_(val_str)
        return val


class DataDir():
    """ directory creation manager """

    def __init__(self, map_, nspecs, depth, source_ddir=None, spec_dfile=None):
        """
        :param map_: maps `nspecs` specifiers to a segment path consisting of
            `depth` directories
        :param info_map_: maps `nspecs` specifiers to an information object, to
            be written in the data directory
        """
        self.map_ = map_
        self.nspecs = nspecs
        self.depth = depth
        self.source = source_ddir
        self.spec_dfile = spec_dfile

    def path(self, prefix, specs=()):
        """ absolute directory path
        """
        if self.source is None:
            pfx = prefix
        else:
            source_specs = self._source_specifiers(specs)
            specs = self._self_specifiers(specs)
            pfx = self.source.path(prefix, source_specs)
        pfx = os.path.abspath(pfx)

        assert len(specs) == self.nspecs

        pth = self.map_(specs)
        assert _path_is_relative(pth)
        assert _path_has_depth(pth, self.depth)
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
        pth = self.path(prefix, specs)
        os.makedirs(pth)

        if self.spec_dfile is not None:
            self.spec_dfile.write(specs, pth)

    def existing(self, prefix, source_specs=()):
        """ return the list of specifiers
        """
        if self.spec_dfile is None:
            raise NotImplementedError

        pths = self.existing_paths(prefix, source_specs)
        specs_lst = tuple(self.spec_dfile.read(pth) for pth in pths)
        return specs_lst

    def existing_paths(self, prefix, source_specs=()):
        """ names of the directories that have been created at this prefix
        """
        if self.source is None:
            pfx = prefix
        else:
            pfx = self.source.path(prefix, source_specs)

        assert os.path.isdir(pfx)
        cwd = os.getcwd()
        os.chdir(pfx)
        pths = sorted(filter(os.path.isdir,
                             glob.glob(os.path.join(*('*' * self.depth)))))
        pths = tuple(os.path.join(pfx, pth) for pth in pths)
        os.chdir(cwd)
        return pths

    # helpers
    def _self_specifiers(self, specs):
        assert len(specs) >= self.nspecs
        return specs[-self.nspecs:]

    def _source_specifiers(self, specs):
        assert len(specs) >= self.nspecs
        return specs[:-self.nspecs]


class DataDirFile():
    """ associates a DataFile with specific DataDir """

    def __init__(self, ddir, dfile):
        self.dir = ddir
        self.file = dfile

    def path(self, prefix, specs=()):
        """ absolute file path
        """
        dir_pth = self.dir.path(prefix, specs)
        return self.file.path(dir_pth)

    def exists(self, prefix, specs=()):
        """ does this file exist?
        """
        dir_pth = self.dir.path(prefix, specs)
        return self.file.exists(dir_pth)

    def write(self, val, prefix, specs=()):
        """ write data to this file
        """
        dir_pth = self.dir.path(prefix, specs)
        self.file.write(val, dir_pth)

    def read(self, prefix, specs=()):
        """ read data from this file
        """
        dir_pth = self.dir.path(prefix, specs)
        return self.file.read(dir_pth)


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


def _specifier_data_file(map_dct_, spec_keys):

    def writer_(specs):
        inf_dct = {key: map_(specs) for key, map_ in map_dct_.items()}
        inf_obj = autoinf.object_(inf_dct)
        return autofile.write.information(inf_obj)

    def reader_(inf_str):
        inf_obj = autofile.read.information(inf_str)
        inf_dct = dict(inf_obj)
        return tuple(map(inf_dct.__getitem__, spec_keys))

    return DataFile(name=autofile.name.information('info'), writer_=writer_,
                    reader_=reader_)


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

    SPEC_DFILE = _specifier_data_file(
        map_dct_={
            'method': lambda specs: specs[0],
            'basis': lambda specs: specs[1],
            'orb_restricted': lambda specs: specs[2]},
        spec_keys=['method', 'basis', 'orb_restricted'])

    DDIR = DataDir(
        map_=(lambda x: autodir.lib.map_.theory_leaf(*x)),
        nspecs=3,
        depth=1,
        source_ddir=SPC_LEAF_DDIR,
        spec_dfile=SPEC_DFILE,
    )

    SPECS = ['InChI=1S/O', 3, 'hf', 'sto-3g', False]
    if not DDIR.exists('.', SPECS):
        DDIR.create('.', SPECS)

    print()
    print(DDIR.existing('.', SPECS[:2]))
