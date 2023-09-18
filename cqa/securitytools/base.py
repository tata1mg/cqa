"""
this module contains the base runner for running all the security 
that are implemented

Author: Shaurya Agarwal
"""

import logging
from typing import Dict, List, Optional

from cqa import utils
from cqa.base import Runner
from cqa.securitytools.bandit import BanditRunner
from cqa.securitytools.detect_secrets import DetectSecretsRunner
from cqa.securitytools.safety import SafetyRunner
from cqa.types import Result


class SecurityTools:

    LOGGER = logging.getLogger(__name__)

    _rootdir: str = ""
    _paths: List[str] = []

    def __init__(
        self,
        paths: List[str],
        rootdir: Optional[str] = None,
        options: Optional[Dict] = None,
    ) -> None:
        if options is None:
            options = {}

        self._runners: List[Runner] = [
            BanditRunner(options.get("bandit", {})),
            DetectSecretsRunner,
        ]

        for path in paths:
            self._paths.extend(utils.walk_path(path))

        self._rootdir = rootdir

    def run(self):
        errors: List = []

        for runner in self._runners:
            errors.extend(runner.run(self._paths, self._rootdir))

        return Result(errors)


class VulnerabilityRunner:
    LOGGER = logging.getLogger(__name__)

    _runners: List[Runner] = [SafetyRunner]

    def __init__(
        self,
        options: Optional[Dict] = None,
    ) -> None:
        if options is None:
            options = {}

    def run(self):
        errors: List = []

        for runner in self._runners:
            errors.extend(runner.run())

        return Result(errors)
