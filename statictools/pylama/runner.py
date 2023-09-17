import tempfile
from argparse import ArgumentParser, Namespace
from typing import Dict, List, Optional

import toml
from pylama.main import check_paths, parse_options

from cqa.base import Runner
from cqa.types import ReporterError, Severity

ERROR_MAPPING: Dict[str, Severity] = {
    "F": Severity.ERROR,
    "E": Severity.ERROR,
    "W": Severity.WARNING,
    "R": Severity.WARNING,
    "C": Severity.WARNING,
}


class PylamaRunner(Runner):
    def __init__(self, options: Optional[Dict] = None):
        if options is None:
            options = {}

        self.options = self.get_config(options)

    def get_config(self, cfg):
        options = Namespace()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml") as temp:
            toml.dump(
                {"tool": {"pylama": cfg}},
                temp,
            )
            temp.flush()
            options = parse_options(["-o", temp.name])
        return options

    def run(self, paths: List[str], rootdir: str) -> List[ReporterError]:
        """
        run pylama for a list of files

        :param paths: (List[str]) files that are to be linted
        :param rootdir: (str) root directory of the project

        :returns: errors found in the file for each file path
        """
        errors: List[ReporterError] = []
        pylama_errors = check_paths(
            paths,
            self.options,
            code=None,
            rootdir=rootdir,
        )

        errors.extend(
            [
                ReporterError(
                    path=error.filename,
                    severity=ERROR_MAPPING.get(error.etype, Severity.WARNING),
                    **(error.to_dict()),
                )
                for error in pylama_errors
            ]
        )

        return errors
