""" common module parameters
"""


class FilePrefix():
    """ file prefixes for different types of information
    """
    RUN = 'run'
    INFO = 'info'
    GEOM = 'geom'
    GRAD = 'grad'
    HESS = 'hess'
    CONF = 'conf'

    # these may need to change downt the road
    LJ = 'lj'
    BATH = 'bath'


class DirectoryName():
    """ names for different types of directories
    """
    RUN = 'run'

    class Run():
        """ run directories """
        OPT = 'opt'
        GRAD = 'grad'
        HESS = 'hess'
