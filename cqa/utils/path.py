import functools
import os
from glob import glob, has_magic
from typing import Callable, Generator, List, Tuple

_EXCLUDED_DIR = ["tests", "build"]


def _walk_file_or_dir(
    root: str,
) -> Generator[Tuple[str, List[str], List[str]], None, None]:
    """
    walk the the root path recursively if its a directory
    otherwise yield the parent directory, directories, and filename

    :param root: (str) path to walk
    :returns: generator to the os.walk object
    """

    if os.path.isfile(root):
        dirname, basename = os.path.split(root)
        yield dirname, [], [basename]
    else:
        for path, dirnames, filenames in os.walk(root):
            yield path, dirnames, filenames


def _is_cqa_eligible_file(path: str) -> bool:
    return (
        os.path.isfile(path)
        and path.endswith(".py")
        and not any([(_exclude in path.lower()) for _exclude in _EXCLUDED_DIR])
    )


@functools.lru_cache()  # Caching because `os.walk` is an expensive process
def walk_path(
    root: str, predicate: Callable[[str], bool] = _is_cqa_eligible_file
) -> List[str]:
    """
    walk the path if its magic path, then match all files matching the pattern
    otherwise walk the os path

    :param root: (str) path/pattern to match all the files
    :returns: list of all the files matching the predicate function
    """

    allfiles = []

    if has_magic(root):
        onlyfiles = [file for file in glob(root) if predicate(file)]
    else:
        path_iter = _walk_file_or_dir(root)
        onlyfiles = [
            os.path.join(parent, file)
            for parent, _, files in path_iter
            for file in files
            if predicate(os.path.join(parent, file))
        ]

    allfiles.extend(onlyfiles)

    return allfiles
