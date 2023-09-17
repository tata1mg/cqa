import os
from typing import Any, Dict, List, Optional

from isort import Config
from isort import check_file as isort_check_file
from isort import file as isort_file

from cqa.base import Runner
from cqa.config import constants
from cqa.types import ReporterError, Severity


class ISortRunner(Runner):
    """
    Runner for isort
    """

    def __init__(self, options: Optional[Dict] = None):
        if options is None:
            options = {}

        self.options = {}  # To use when config needs to be overridden
        options = self.get_config(options)
        self.config = Config(**options)

    def get_config(self, cfg: Dict[str, Any]):
        return {k.replace("-", "_"): v for k, v in cfg.items()}

    def run(
        self, paths: List[str], rootdir: Optional[str] = None
    ) -> List[ReporterError]:
        """
        run isort for the given list of files

        :param paths: (List[str]) paths of files to be formatted
        :param rootdir: (str) path of the root directory

        :returns: List of files that have been modified
        """

        errors: List[ReporterError] = []
        for path in paths:
            self.LOGGER.info("sorting imports for path: %s", path)
            is_changed = self._format_or_check(
                path,
                rootdir,
                check_only=False,
                config=self.config,
                options=self.options,
            )

            if is_changed:
                errors.append(
                    ReporterError(
                        path=path,
                        message=constants.ISORT_ERROR_MSG,
                        severity=Severity.WARNING,
                    )
                )

        return errors

    def _format_or_check(
        self,
        path: str,
        rootdir: str,
        check_only: Optional[bool] = True,
        config: Optional[Config] = None,
        options: Optional[Dict] = None,
    ):
        if options is None:
            options = {}

        if path is not None:
            path = os.path.relpath(path, rootdir)

        if check_only:
            return isort_check_file(path, config=config, **options)
        else:
            return isort_file(path, config=config, **options)
