import contextlib
import shlex
import sys
from typing import List
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from cqa.cli.args import get_args
from tests.testutils import _test_cwd, constants, create_files, destroy_files


class CliTests(TestCase):
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
    def test_cli_argument_deduplication(self, filepaths: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa -l INFO run --path")
        testargs.extend(filepaths)
        testargs.extend("--path")
        testargs.extend(filepaths)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))

            # Execute
            with patch("sys.exit") as context:
                _args = get_args()

                # Verify
                self.assertTrue(context.called)

    @parameterized.expand([(_files_created, _rootdir)])
    def test_cl_argument_success(self, filepaths: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa -l INFO run --path")
        testargs.extend(filepaths)

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))

            # Execute
            args = get_args()

            # Verify
            self.assertFalse(args.format)
            self.assertEqual(args.path, filepaths)
            self.assertEqual(args.action, "run")
            self.assertEqual(args.logLevel, "INFO")

    @parameterized.expand([([], _rootdir)])
    def test_cli_no_path_argument(self, filepaths: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa -l INFO run")

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))

            # Execute
            with patch("sys.exit") as context:
                _args = get_args()

                # Verify
                self.assertTrue(context.called)
                self.assertEqual(
                    context.call_args[0][0], "Error: --path argument is required"
                )

    @parameterized.expand([(["-l", "FOO"], _rootdir)])
    def test_cli_invalid_log_level(self, testargs: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa")
        testargs.extend(testargs)
        testargs.extend(["run", "--path", "a/b/c.py"])

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))

            # Execute
            with patch("sys.exit") as context:
                _args = get_args()

                # Verify
                self.assertTrue(context.called)
                self.assertEqual(
                    context.call_args[0][0],
                    "Error: Invalid value for --logLevel argument: FOO",
                )

    @parameterized.expand([(["--action", "foo"], _rootdir)])
    def test_cli_invalid_action(self, testargs: List[str], rootdir: str):
        # Prepare
        testargs = shlex.split("cqa")
        testargs.extend(testargs)
        testargs.extend(["--path", "a/b/c.py"])

        with contextlib.ExitStack() as stack:
            stack.enter_context(_test_cwd(rootdir))
            stack.enter_context(patch.object(sys, "argv", testargs))

            # Execute
            with patch("sys.exit") as context:
                _args = get_args()

                # Verify
                self.assertTrue(context.called)
                self.assertEqual(context.call_args[0][0], "Error: Invalid action: foo")
