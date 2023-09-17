import contextlib
import os
import shutil
from pathlib import Path
from typing import List, Union

import tests.testutils.constants as constants


@contextlib.contextmanager
def _test_cwd(current_working_directory: Union[str, Path, None] = None):
    """
    Sets the <current_working_directory>

    :param str current_working_directory: path of directory to be set
    """

    cwd = os.getcwd()
    try:
        if current_working_directory is not None:
            os.chdir(current_working_directory)
        yield
    finally:
        os.chdir(cwd)


def create_files(
    paths: List[str],
    permission: int = 0o660,
    chroot: str = constants.TEMP_DIR,
) -> None:
    """
    Creates directories and files found in <path>.

    :param list paths: list of relative paths to files or directories
    :param int permission: linux permission value of the files to be created
    :param str chroot: the root directory in which paths will be created
    """
    dirs, files = set(), set()
    for path in paths:
        path = os.path.join(chroot, path)
        filename = os.path.basename(path)
        # path is a directory path
        if not filename:
            dirs.add(path)
        # path is a filename path
        else:
            dirs.add(os.path.dirname(path))
            files.add(path)
    for dirpath in dirs:
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
    for filepath in files:
        with open(filepath, "w", encoding="utf-8"):
            pass
        os.chmod(filepath, permission)  # change the permission of the file


def destroy_files(paths: List[str], chroot: str = constants.TEMP_DIR):
    """
    Deletes directories / files for the given <paths>

    :param list paths: list of paths of files and directories to delete
    """
    for path in paths:
        path = os.path.join(chroot, path)
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
