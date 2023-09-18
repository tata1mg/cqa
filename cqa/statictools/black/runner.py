import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from black import Mode, WriteBack, format_file_in_place
from black.mode import TargetVersion

from cqa.base import Runner
from cqa.config.constants import FILE_FORMATTED_ERROR
from cqa.types import ReporterError, Severity


class BlackRunner(Runner):
    """
    runner for black formatter
    """

    def __init__(self, options: Optional[Dict] = None):
        if options is None:
            options = {}

        self._options = self.get_config(options)

    def get_config(self, cfg: Dict[str, Any]):
        config = {k.replace("--", "").replace("-", "_"): v for k, v in cfg.items()}
        target_versions = config.get("target_versions", set())
        config["target_versions"] = [
            TargetVersion[val.upper()] for val in target_versions
        ]

        return {
            "fast": True,
            "mode": Mode(**config),
            "write_back": WriteBack.YES,
        }

    def run(self, paths: List[str], rootdir: str):
        errors: List[ReporterError] = []
        for path in paths:
            self.LOGGER.info("formatting file %s using black formatter", path)
            errors.append(self._parse_single_file(path, rootdir, self._options))
        return errors

    def _parse_single_file(
        self,
        path: str,
        rootdir: Optional[str] = None,
        options: Optional[Dict] = None,
    ):
        if options is None:
            options = {}

        if rootdir is not None:
            path = os.path.relpath(path, rootdir)

        changed = format_file_in_place(Path(path), **options)
        if changed:
            error_msg = FILE_FORMATTED_ERROR.format(path=path, linter="black")
            return ReporterError(
                path=path,
                message=error_msg,
                severity=Severity.ERROR,
            )

        return ReporterError(severity=Severity.WARNING)  # NULL Warning if not modified
