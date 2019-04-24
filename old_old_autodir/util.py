""" some common utilities
"""
import os
import autofile


def create_directory(prefix, dir_path):
    """ create directory branch at this prefix
    """
    prefix = os.path.abspath(prefix)
    dir_path = os.path.abspath(dir_path)
    assert os.path.isdir(prefix)
    assert os.path.commonprefix([prefix, dir_path]) == prefix
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


class DataFile():
    """ a class implementing common data file methods """

    def __init__(self, file_name, dir_path_,
                 writer_=(lambda _: _), reader_=(lambda _: _),
                 checker_=(lambda _: True)):
        """
        :param dir_path_: assigns directory path from arguments
        :type dir_path: callable[*args->str]
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        :param checker_: checks data validity upon reading/writing
        :type checker_: callable[object->bool]
        """
        self.file_name = file_name
        self.dir_path_ = dir_path_
        self.writer_ = writer_
        self.reader_ = reader_
        self.checker_ = checker_

    def path(self, args):
        """ get the file path
        """
        dir_path = self.dir_path_(*args)
        return os.path.join(dir_path, self.file_name)

    def exists(self, args):
        """ does this file exist
        """
        file_path = self.path(args)
        return os.path.isfile(file_path)

    def write(self, args, file_dat):
        """ write the data to file
        """
        assert self.checker_(file_dat)
        file_path = self.path(args)
        file_str = self.writer_(file_dat)
        autofile.write_file(file_path, file_str)

    def read(self, args):
        """ read the data from a file
        """
        assert self.exists(args=args)
        file_path = self.path(args)
        file_str = autofile.read_file(file_path)
        file_dat = self.reader_(file_str)
        assert self.checker_(file_dat)
        return file_dat
