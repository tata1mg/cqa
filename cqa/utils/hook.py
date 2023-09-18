import os
import stat

import git

from .cmd import get_lines


def install_git_hook(precommit_file: str = "hooks/pre-commit"):
    bash_script = """
files=$(git diff-index --cached --name-only HEAD)
if [ -z "$files" ]
then
    echo "error: there are no files staged, please stage some files to run cqa"
    echo "exiting..."
    exit 1
else
    cqa run --path $files --fail --format
fi
    """

    repo = git.Repo(".", search_parent_directories=True)
    if not repo.git_dir:
        raise AssertionError(
            "not a git repository (or any \
            of the parent directories)"
        )

    precommit_file = os.path.join(repo.git_dir, precommit_file)
    with open(precommit_file, "w", encoding="utf-8") as file:
        file.write(bash_script)
        st = os.stat(precommit_file)
        os.chmod(precommit_file, mode=st.st_mode | stat.S_IEXEC)


def git_hook(path: str = "", strict: bool = False, lazy: bool = True) -> int:
    """
    git pre-commit hook to check staged files for isort errors

    :param strict: (bool) - if True, return number of errors on exit,
        causing the hook to fail. If False, return zero so it will
        just act as a warning.
    :param modify: (bool) - if True, fix the sources if they are not
        sorted properly. If False, only report result without
        modifying anything.
    :param lazy: (bool) - if True, also check/fix unstaged files.
        This is useful if you frequently use ``git commit -a`` for example.
        If False, only check/fix the staged files for isort errors.
    :returns: number of errors if in strict mode, 0 otherwise.
    """
    # Get list of files modified and staged
    diff_cmd = [
        "git",
        "diff-index",
        "--cached",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        "HEAD",
        path,
    ]
    if lazy:
        diff_cmd.remove("--cached")

    files_modified = get_lines(diff_cmd)
    if not files_modified:
        return 0

    errors = 0

    for filename in files_modified:
        if filename.endswith(".py"):
            # Get the staged contents of the file
            pass

    return errors if strict else 0
