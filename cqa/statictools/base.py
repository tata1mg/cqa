import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set

from cqa import utils
from cqa.base import Runner
from cqa.types import Result


class Linter:
    """
    static code tools runner
    """

    LOGGER = logging.getLogger(__name__)

    _linters: Set[Runner] = set()

    _rootdir: str = ""
    _paths: Set[str] = set()
    _options: Dict = {}

    def __init__(self, paths: List[str], rootdir: str, options: Dict = None):
        # Below changes done to improve cqa commands speed(except run),
        # Below imports were slowing general commands
        from cqa.statictools.pylama import PylamaRunner  # noqa
        from cqa.statictools.pytype import PytypeRunner  # noqa

        self._linters = {
            PylamaRunner(options.get("pylama", {})),
            PytypeRunner(),
        }

        if options is None:
            options = {}

        for path in paths:
            walked = set(utils.walk_path(path))
            self._paths.update(walked)

        self._rootdir = rootdir
        self._options.update(options)

    def run(self):
        errors: List = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            _futures = []
            for linter in self._linters:
                self.LOGGER.info(
                    "linting using linter: %s",
                    linter.__class__.__name__,
                )
                _futures.append(
                    executor.submit(linter.run, self._paths, self._rootdir),
                )

            for _fut in as_completed(_futures):
                errors.extend(_fut.result())

        return Result(errors)


class Formatter:
    LOGGER = logging.getLogger(__name__)

    _formatters: Set[Runner] = set()

    _rootdir: str = ""
    _options: Dict = {}
    _paths: Set[str] = set()

    def __init__(
        self,
        paths: Set[str],
        rootdir: str,
        options: Optional[Dict] = None,
    ):
        from cqa.statictools.black import BlackRunner  # noqal
        from cqa.statictools.isort import ISortRunner  # noqa

        self._formatters = {
            ISortRunner(options.get("isort", {})),
            BlackRunner(options.get("black", {})),
        }
        if options is None:
            options = {}

        for path in paths:
            self._paths = self._paths.union(utils.walk_path(path))

        self._rootdir = rootdir
        self._options.update(options)

    def run(self):
        errors: List = []
        for formatter in self._formatters:
            self.LOGGER.info(
                "formatting code using formatter %s",
                formatter,
            )
            errors.extend(formatter.run(self._paths, self._rootdir))
        return Result(errors)
