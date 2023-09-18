import tempfile
from typing import Any, Dict, List, Optional

import toml
from bandit import config as b_config
from bandit import constants as b_constants
from bandit import manager as b_manager

from cqa.base import Runner
from cqa.types import ReporterError, Severity


class BanditRunner(Runner):
    """
    runner for bandit to check for security vulnerabilities in
    the code through static analysis
    """

    SEVERITY_MAP = {
        "LOW": Severity.WARNING,
        "MEDIUM": Severity.ERROR,
        "HIGH": Severity.ERROR,
    }

    def __init__(self, options: Optional[Dict] = None):
        config = self.get_config(options)
        self.manager: b_manager.BanditManager = b_manager.BanditManager(
            config=config, agg_type=None
        )

    def get_config(self, cfg: Dict[str, Any]):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml") as temp:
            toml.dump({"tool": {"bandit": cfg}}, temp)
            temp.flush()
            return b_config.BanditConfig(temp.name)

    def run(self, paths: List[str], rootdir: str) -> List[ReporterError]:
        """
        run the bandit runner to discover security flaws in the given paths

        :param paths: (List[str]) list of paths for which to run bandit
                    security analysis
        :param rootdir: (str) root directory of the project
        :returns: list of errors reported by bandit
        """

        self.manager.discover_files(paths, recursive=False)
        self.manager.run_tests()

        issues = self.manager.get_issue_list(b_constants.LOW, b_constants.LOW)
        results = [
            ReporterError(
                path=issue.fname,
                message=issue.text,
                lnum=issue.lineno,
                severity=self.SEVERITY_MAP.get(
                    issue.severity,
                    Severity.WARNING,
                ),
                confidence=issue.confidence,
            )
            for issue in issues
        ]

        return results
