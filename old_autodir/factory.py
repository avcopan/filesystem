""" generic classes defining structure of the filesystem API
"""
import os
import glob
import types
import itertools
import autofile


class DataDir():
    """ a class implementing common data directory methods """

    def __init__(self, name_, nargs=0, depth=1,
                 creation_side_effect_=(lambda _1, _2: None)):
        """
        :param name_: gets directory name from arguments
        :type name_: callable[args->str]
        :param creation_side_effect_: does something after the directory is
            created
        :type creation_side_effect_: callable[prefix,args->None]
        """
        self.name_ = name_
        self.nargs = nargs
        self.depth = depth
        self.creation_side_effect_ = creation_side_effect_

    def path(self, prefix, args=()):
        """ get the directory path
        """
        assert len(args) == self.nargs
        prefix = os.path.abspath(prefix)
        name = self.name_(args)
        assert os.path.relpath(name) == name
        assert len(_os_path_split_all(name)) == self.depth
        return os.path.join(prefix, name)

    def exists(self, prefix, args=()):
        """ does this directory exist?
        """
        dir_path = self.path(prefix, args)
        return os.path.isdir(dir_path)

    def create(self, prefix, args=()):
        """ create a directory at this prefix
        """
        assert os.path.isdir(prefix)
        assert not self.exists(prefix, args)
        dir_path = self.path(prefix, args)
        os.makedirs(dir_path)

        self.creation_side_effect_(prefix, args)

    def created_names(self, prefix):
        """ names of the directories that have been created at this prefix
        """
        assert os.path.isdir(prefix)
        cwd = os.getcwd()
        os.chdir(prefix)
        names = tuple(sorted(filter(
            os.path.isdir,
            glob.glob(os.path.join(*('*' * self.depth))))))
        os.chdir(cwd)
        return names

    def stacked_over(self, base_ddir):
        """ get a copy of this DataDir stacked over a base DataDir
        """
        nargs = base_ddir.nargs + self.nargs
        depth = base_ddir.depth + self.depth

        def name_(args):
            base_args = args[:base_ddir.nargs]
            args = args[base_ddir.nargs:]
            return os.path.join(base_ddir.name_(base_args), self.name_(args))

        def creation_side_effect_(prefix, args):
            base_prefix = prefix
            base_args = args[:base_ddir.nargs]

            prefix = base_ddir.path(base_prefix, base_args)
            args = args[base_ddir.nargs:]

            base_ddir.creation_side_effect_(base_prefix, base_args)
            self.creation_side_effect_(prefix, args)

        return DataDir(name_=name_, nargs=nargs, depth=depth,
                       creation_side_effect_=creation_side_effect_)


class DataFile():
    """ a class implementing common data file methods """

    def __init__(self, ddir, name, writer_=(lambda _: _),
                 reader_=(lambda _: _)):
        """
        :param ddir: a DataDir object specifying the directory for the file
        :type ddir: DataDir
        :param name: the file name
        :type name: str
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        """
        self.dir = ddir
        self.name = name
        self.writer_ = writer_
        self.reader_ = reader_

    def path(self, prefix, args=()):
        """ get the file path
        """
        dir_path = self.dir.path(prefix, args)
        return os.path.join(dir_path, self.name)

    def exists(self, prefix, args=()):
        """ does this file exist?
        """
        file_path = self.path(prefix, args)
        return os.path.isfile(file_path)

    def write(self, val, prefix, args=()):
        """ write the data to file
        """
        file_path = self.path(prefix, args)
        val_str = self.writer_(val)
        autofile.write_file(file_path, val_str)

    def read(self, prefix, args=()):
        """ read the data from a file
        """
        assert self.exists(prefix, args)
        file_path = self.path(prefix, args)
        val_str = autofile.read_file(file_path)
        val = self.reader_(val_str)
        return val

    def stacked_over(self, base_ddir):
        """ get a copy of this DataFile stacked over a base DataDir
        """
        ddir = self.dir.stacked_over(base_ddir)
        return DataFile(ddir=ddir, name=self.name, writer_=self.writer_,
                        reader_=self.reader_)


class DataLayer():
    """ a single-layered system of directories and files """

    def __init__(self, ddir, dfile_dct=None):
        """
        :param ddir: a DataDir object
        :param dfiles: a sequence of pairs `(name, obj)` where `obj` is a
            DataFile instance that will be accessible as `obj.file.name`
        """
        dfile_dct = {} if dfile_dct is None else dfile_dct

        assert isinstance(ddir, DataDir)
        self.dir = ddir
        self.file = types.SimpleNamespace()
        for name, obj in dfile_dct.items():
            assert isinstance(name, str)
            assert isinstance(obj, DataFile)
            setattr(self.file, name, obj)

    def stacked_over(self, base_ddir):
        """ get a copy of this DataLayer stacked over a base DataDir
        """
        ddir = self.dir.stacked_over(base_ddir)
        dfile_dct = {name: obj.stacked_over(base_ddir)
                     for name, obj in vars(self.file).items()}
        return DataLayer(ddir=ddir, dfile_dct=dfile_dct)


class FileSystem(types.SimpleNamespace):
    """ a collection of DataLayers """

    def __init__(self, dlayer_dct):
        for name, obj in dlayer_dct.items():
            assert isinstance(name, str)
            assert isinstance(obj, DataLayer)
            setattr(self, name, obj)

    @staticmethod
    def by_stacking(dlayer_seq):
        """ create a FileSystem by stacking DataLayers
        """
        names, objs = zip(*dlayer_seq)
        assert len(set(names)) == len(names)
        objs = list(itertools.accumulate(
            objs, (lambda x, y: y.stacked_over(x.dir))))
        dlayer_dct = dict(zip(names, objs))
        return FileSystem(dlayer_dct=dlayer_dct)


# helpers
def _os_path_split_all(path):
    """ grabbed this from the internet """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:    # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
