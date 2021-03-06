""" defines the filesystem model for autodir
"""
import os
import glob
import autofile


class DataFile():
    """ file manager for a given datatype """

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


class DataSeriesDir():
    """ directory manager mapping specifier values to a directory series
    """

    def __init__(self, map_, nspecs, depth, spec_dfile=None,
                 source_dsdir=None):
        """
        :param map_: maps `nspecs` specifiers to a segment path consisting of
            `depth` directories
        :param info_map_: maps `nspecs` specifiers to an information object, to
            be written in the data directory
        """
        self.map_ = map_
        self.nspecs = nspecs
        self.depth = depth
        self.spec_dfile = spec_dfile
        self.source = source_dsdir

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
        # recursively create starting from the first source directory
        if self.source is not None:
            source_specs = self._source_specifiers(specs)
            self.source.create(prefix, source_specs)

        # create this directory in the chain, if it doesn't already exist
        assert os.path.isdir(prefix)
        if not self.exists(prefix, specs):
            pth = self.path(prefix, specs)
            os.makedirs(pth)

            if self.spec_dfile is not None:
                specs = self._self_specifiers(specs)
                self.spec_dfile.write(specs, pth)

    def existing(self, prefix, source_specs=()):
        """ return the list of specifiers
        """
        if self.spec_dfile is None:
            raise ValueError("This function does not work "
                             "without a specifier DataFile")

        pths = self.existing_paths(prefix, source_specs)
        specs_lst = tuple(sorted(self.spec_dfile.read(pth) for pth in pths))
        return specs_lst

    def existing_paths(self, prefix, source_specs=()):
        """ specifiers for all existing paths at this prefix/source directory
        """
        if self.source is None:
            pfx = prefix
        else:
            pfx = self.source.path(prefix, source_specs)

        pfx = os.path.abspath(pfx)
        assert os.path.isdir(pfx)

        pth_pattern = os.path.join(pfx, *('*' * self.depth))
        pths = filter(os.path.isdir, glob.glob(pth_pattern))
        pths = tuple(os.path.join(pfx, pth) for pth in pths)
        return pths

    # helpers
    def _self_specifiers(self, specs):
        """ specifiers for this DataSeriesDir
        """
        nspecs = len(specs)
        assert nspecs >= self.nspecs
        source_nspecs = nspecs - self.nspecs
        return specs[source_nspecs:]

    def _source_specifiers(self, specs):
        """ specifiers for the source DataSeriesDir, if there is one
        """
        nspecs = len(specs)
        assert nspecs >= self.nspecs
        source_nspecs = nspecs - self.nspecs
        return specs[:source_nspecs]


class DataSeriesFile():
    """ file manager mapping specifier values to files in a directory series
    """

    def __init__(self, dsdir, dfile):
        self.dir = dsdir
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


if __name__ == '__main__':
    import autodir.lib

    SPC_TRUNK_DSDIR = autodir.lib.dir_.species_trunk()
    SPC_LEAF_DSDIR = autodir.lib.dir_.species_leaf(SPC_TRUNK_DSDIR)
    THY_LEAF_DSDIR = autodir.lib.dir_.theory_leaf(SPC_LEAF_DSDIR)

    SPECS = ['InChI=1S/O', 3, 'hf', 'sto-3g', False]
    if not THY_LEAF_DSDIR.exists('.', SPECS):
        THY_LEAF_DSDIR.create('.', SPECS)

    print()
    print(SPC_LEAF_DSDIR.existing('.'))
    print(THY_LEAF_DSDIR.existing('.', SPECS[:2]))
