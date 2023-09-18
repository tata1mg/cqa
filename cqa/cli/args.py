import os
import argparse

from .actions import Once


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--log",
        dest="logLevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="set the logging level",
    )

    subparser = parser.add_subparsers(dest="action", required=True)

    hookparser = subparser.add_parser(
        "hook",
        help="for options regarding the git hook",
    )
    hookparser.add_argument(
        "--install",
        action="store_true",
        default=False,
        dest="install_git_hook",
        required=True,
        help="install the CQA tool as a git pre-commit hook",
    )

    runparser = subparser.add_parser(
        "run",
        help="run the given static code analysis tools on the given paths",
    )
    runparser.add_argument(
        "--format",
        action="store_true",
        default=False,
        help="flag to format the given files as well or not",
    )
    runparser.add_argument(
        "--path",
        nargs="+",
        default=".",
        action=Once,
        help="path of the files that are to be analysed",
    )
    runparser.add_argument(
        "--fail",
        action="store_true",
        dest="fail",
        help="flag determines if it should fail upon finding an error or not",
    )
    runparser.add_argument(
        "--config",
        default=os.path.join(os.getcwd(), "pyproject.toml"),
        help="path of the toml configuration file (default = ./pyproject.toml)",
    )

    return parser.parse_args()
