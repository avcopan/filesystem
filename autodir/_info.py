""" information file handling
"""
import os
import itertools
import yaml

INFO_FILE_NAME = 'info.yaml'


def file_specs(dir_names, info_dcts):
    """ a dictionary of file strings keyed by file path
    """
    dir_paths = tuple(itertools.accumulate(dir_names, os.path.join))
    file_paths = tuple(os.path.join(dir_path, INFO_FILE_NAME)
                       for dir_path in dir_paths)
    file_strs = tuple(_yaml_string(info_dct) if info_dct is not None else None
                      for info_dct in info_dcts)

    assert len(file_paths) == len(file_strs)
    spec_dct = {file_path: file_str
                for file_path, file_str in zip(file_paths, file_strs)
                if file_str is not None}
    return spec_dct


def _yaml_string(dct):
    return yaml.dump(dct, default_flow_style=False)
