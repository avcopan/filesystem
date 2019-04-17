""" test the autodir module
"""
import os
import tempfile
import autodir

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__factory():
    """ test autodir.factory
    """
    def _name(args):
        num, = args
        assert isinstance(num, int)
        pth = str(num)
        return pth

    def _path_inv(prefix, pth):
        assert prefix
        args = (int(pth),)
        return args

    ref_args_lst = tuple((i,) for i in range(10))
    ref_vals = tuple(float(i) / 2 for i in range(10))
    prefix = os.path.join(TMP_DIR, 'factory')
    os.mkdir(prefix)

    fsys = autodir.factory.DataLayer(
        ddir=autodir.factory.DataDir(_name, _path_inv),
        dfile_dct={
            'energy': autodir.lib.dfile.energy(
                dir_name_=_name, file_prefix='file_prefix')})

    for args, val in zip(ref_args_lst, ref_vals):
        assert not fsys.dir.exists(prefix, args)
        fsys.dir.create(prefix, args)
        assert fsys.dir.exists(prefix, args)

        assert not fsys.file.energy.exists(prefix, args)
        fsys.file.energy.write(prefix, args, val)
        assert fsys.file.energy.exists(prefix, args)

    args_lst = fsys.dir.created(prefix)
    assert args_lst == ref_args_lst

    vals = tuple(fsys.file.energy.read(prefix, args) for args in args_lst)
    assert vals == ref_vals

    print(args_lst)
    print(vals)


if __name__ == '__main__':
    test__factory()
