""" directory creation utilities
"""
import os.path


def create(prefix, schem):
    """ create directory and files for a given schema
    """
    assert os.path.isdir(prefix)

    dir_path, file_spec_dct = _validate_schem(schem)

    file_paths = tuple(file_spec_dct.keys())
    file_strs = tuple(file_spec_dct.values())

    dir_path = _normalized_path(prefix, dir_path)
    file_paths = tuple(_normalized_path(prefix, file_path)
                       for file_path in file_paths)

    # make sure each file is in this branch:
    assert all(os.path.commonpath([dir_path, file_path]) ==
               os.path.dirname(file_path) for file_path in file_paths)

    # create the directory path
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write the information files
    for file_path, file_str in zip(file_paths, file_strs):
        _write(file_path, file_str)

    return dir_path


def _validate_schem(schem):
    assert len(schem) == 2

    dir_path, file_spec_dct = schem
    assert isinstance(dir_path, str)
    assert isinstance(file_spec_dct, dict)
    assert not os.path.isabs(dir_path)
    assert not any(map(os.path.isabs, file_spec_dct))
    return schem


def _normalized_path(prefix, path):
    assert not os.path.isabs(path)
    return os.path.abspath(os.path.join(prefix, path))


def _write(file_path, file_str):
    with open(file_path, 'w') as file_obj:
        file_obj.write(file_str)
