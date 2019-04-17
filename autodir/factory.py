""" generic classes defining structure of the filesystem API
"""
import os
import types
import autofile


class DataDir():
    """ a class implementing common data directory methods """

    def __init__(self, name_, path_inv_=None, create_side_effect_=None):
        """
        :param name_: gets directory name from arguments
        :type name_: callable[args->str]
        :param path_inv_: recovers creation arguments from the prefix and the
            directory name
        :type path_inv_: callable[str,str->args]
        :param create_side_effect_: does something after the directory is
            created
        :type create_side_effect_: callable[prefix,args->None]
        """
        self.name_ = name_
        self.path_inv_ = path_inv_
        self.create_side_effect_ = create_side_effect_

    def path(self, prefix, args):
        """ get the directory path
        """
        prefix = os.path.abspath(prefix)
        name = self.name_(args)
        assert os.path.relpath(name) == name
        return os.path.join(prefix, name)

    def exists(self, prefix, args):
        """ does this directory exist?
        """
        dir_path = self.path(prefix, args)
        return os.path.isdir(dir_path)

    def create(self, prefix, args):
        """ create a directory at this prefix
        """
        assert os.path.isdir(prefix)
        assert not self.exists(prefix, args)
        dir_path = self.path(prefix, args)
        os.makedirs(dir_path)

        if self.create_side_effect_ is not None:
            self.create_side_effect_(prefix, args)

    def created(self, prefix):
        """ args for the directories that have been created at this prefix
        """
        if self.path_inv_ is None:
            raise NotImplementedError

        assert os.path.isdir(prefix)
        dir_names = sorted(next(os.walk(prefix))[1])
        args_lst = tuple([self.path_inv_(prefix, name) for name in dir_names])
        return args_lst


class DataFile():
    """ a class implementing common data file methods """

    def __init__(self, dir_name_, file_name,
                 writer_=(lambda _: _), reader_=(lambda _: _)):
        """
        :param dir_name_: gets directory name from arguments
        :type dir_path: callable[args->str]
        :param file_name: the file name
        :type file_name: str
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        """
        self.dir_obj = DataDir(name_=dir_name_)
        self.file_name = file_name
        self.dir_name_ = dir_name_
        self.writer_ = writer_
        self.reader_ = reader_

    def path(self, prefix, args):
        """ get the file path
        """
        dir_path = self.dir_obj.path(prefix, args)
        return os.path.join(dir_path, self.file_name)

    def exists(self, prefix, args):
        """ does this file exist?
        """
        file_path = self.path(prefix, args)
        return os.path.isfile(file_path)

    def write(self, prefix, args, val):
        """ write the data to file
        """
        file_path = self.path(prefix, args)
        val_str = self.writer_(val)
        autofile.write_file(file_path, val_str)

    def read(self, prefix, args):
        """ read the data from a file
        """
        assert self.exists(prefix, args)
        file_path = self.path(prefix, args)
        val_str = autofile.read_file(file_path)
        val = self.reader_(val_str)
        return val


class DataLayer():
    """ creates a one-directory-deep file system """

    def __init__(self, ddir, dfile_dct=None):
        """
        :param ddir: a DataDir object
        :param dfile_dct: a dictionary of DataFile's by attribute name -- these
            will be accessible as obj.file.attr_name
        """
        dfile_dct = {} if dfile_dct is None else dfile_dct

        assert isinstance(ddir, DataDir)
        assert isinstance(dfile_dct, dict)
        self.dir = ddir
        self.file = types.SimpleNamespace()
        for key, val in dfile_dct.items():
            assert isinstance(val, DataFile) and val.dir_name_ == ddir.name_
            setattr(self.file, key, val)
