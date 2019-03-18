""" read/write quantum chemistry data in standard formats
"""
from autofile import name
from autofile import write
from autofile import read
from autofile._util import read_file
from autofile._util import write_file

__all__ = [
    'name',
    'write',
    'read',
    'write_file',
    'read_file',
]
