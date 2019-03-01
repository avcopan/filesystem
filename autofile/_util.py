""" utilities
"""


def read_file(file_path):
    """ read a file as a string
    """
    with open(file_path, 'r') as file_obj:
        file_str = file_obj.read()
    return file_str


def write_file(file_path, string):
    """ write a string to a file
    """
    with open(file_path, 'w') as file_obj:
        file_obj.write(string)
