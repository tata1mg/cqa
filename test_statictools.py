import contextlib
import shlex
import sys
from typing import List
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from cqa.cli.args import get_args
from cqa.statictools.base import StaticCodeTools
from cqa.types import ReporterError
from tests.testutils import _test_cwd, constants, create_files, destroy_files


class StaticCodeToolTests(TestCase):
    _rootdir = constants.TEMP_DIR
    _files_created: List[str] = ["a/b/c.py", "a/b/d/e.py"]

    def setUp(self):
        create_files(self._files_created, chroot=constants.TEMP_DIR)
        super().setUp()

    def tearDown(self) -> None:
        destroy_files(self._files_created, chroot=constants.TEMP_DIR)
        return super().tearDown()

    def doCleanups(self) -> None:
        destroy_files(
            [], chroot=constants.TEMP_DIR
        )  # destroy all the files in the default rootdir
        return super().doCleanups()

    @parameterized.expand([(_files_created, _rootdir)])
    def test_missing_docstring(self, filepaths: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa run --path")
        testargs.extend(filepaths)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))
            args = get_args()

            # Execute
            statictools = StaticCodeTools(paths=args.path, rootdir=rootdir)
            errors = statictools.run(modify=args.format)

            # Verify
            self.assertIn(
                ReporterError(path="a/b/c.py", message=constants.MISSING_DOCSTRING),
                errors,
            )
            self.assertIn(
                ReporterError(path="a/b/d/e.py", message=constants.MISSING_DOCSTRING),
                errors,
            )

    @parameterized.expand([(_files_created, _rootdir)])
    def test_no_errors(self, filepaths: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa run --path")
        testargs.extend(filepaths)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))
            args = get_args()

            # Execute
            statictools = StaticCodeTools(paths=args.path, rootdir=rootdir)
            errors = statictools.run(modify=args.format)

            self.assertEqual([], errors)

    @parameterized.expand([(["--format", "foo"], _files_created, _rootdir)])
    def test_invalid_format(
        self, testargs: List[str], filepaths: List[str], rootdir: str
    ):
        # Prepare
        testargs = shlex.split("cqa run")
        testargs.extend(testargs)
        testargs.extend(["--path"])
        testargs.extend(filepaths)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))
            args = get_args()

            # Execute and verify
            statictools = StaticCodeTools(paths=args.path, rootdir=rootdir)
            with self.assertRaises(ValueError):
                statictools.run(modify=args.format)

    @parameterized.expand([(["--path", "foo/bar.py"], _files_created, _rootdir)])
    def test_nonexistent_file(
        self, testargs: List[str], filepaths: List[str], rootdir: str
    ):
        # Prepare
        testargs = shlex.split("cqa run")
        testargs.extend(testargs)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))
            args = get_args()

            # Execute and verify
            statictools = StaticCodeTools(paths=args.path, rootdir=rootdir)
            with self.assertRaises(FileNotFoundError):
                statictools.run(modify=args.format)
