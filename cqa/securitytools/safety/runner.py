import os
from typing import Dict, Generator, List, Optional

from dparse import filetypes, parse
from safety.models import Package, Vulnerability
from safety.safety import check

from cqa.base import Runner
from cqa.types import PackageVulnerability


class SafetyRunner(Runner):
    _options: Dict = {}

    def __init__(self, options: Optional[Dict] = None):
        if options is None:
            options = {}

        self._options.update(options)

    rootdir = ""

    @classmethod
    def run(
        cls,
        _paths: Optional[List[str]] = None,
        rootdir: Optional[str] = "",
    ):
        cls.rootdir = rootdir
        requirements = cls._get_packages()
        issues = check(requirements, ignore_vulns=[])
        if not issues[0] and not issues[1]:
            return []

        errors: List[PackageVulnerability] = []
        for pkg_issues in issues:
            for vuln in pkg_issues:
                if isinstance(vuln, Vulnerability):
                    errors.append(
                        PackageVulnerability(
                            vulnerability_id=vuln.vulnerability_id,
                            package_name=vuln.pkg.name,
                            current_version=vuln.pkg.version,
                            affected_versions=vuln.all_vulnerable_specs,
                            cvssv2_score=vuln.CVE.cvssv2,
                            cvssv3_score=vuln.CVE.cvssv3,
                            advisory=vuln.advisory,
                            more_info_url=vuln.more_info_url,
                        )
                    )
        return errors

    @classmethod
    def _get_packages(cls):
        content = ""
        file_type = None

        if os.path.exists(os.path.join(cls.rootdir, "Pipfile.lock")):
            with open(
                os.path.join(cls.rootdir, "Pipfile.lock"),
                "r",
                encoding="utf-8",
            ) as file:
                content = file.read()
                file_type = filetypes.pipfile_lock
        elif os.path.exists(
            os.path.join(
                cls.rootdir,
                cls._options.get("requirements_file", "requirements.txt"),
            )
        ):
            with open(
                os.path.join(
                    cls.rootdir,
                    cls._options.get("requirements_file", "requirements.txt"),
                ),
                "r",
                encoding="utf-8",
            ) as file:
                content = file.read()
                file_type = filetypes.requirements_txt
        else:
            return []

        requirements = list(
            cls._parse_requirements(content=content, file_type=file_type)
        )
        return requirements

    @classmethod
    def _parse_requirements(
        cls,
        content: str,
        path: Optional[str] = None,
        file_type: Optional[str] = filetypes.requirements_txt,
        resolve: bool = True,
    ) -> Generator[None, None, Package]:
        dependency_file = parse(
            content, path=path, resolve=resolve, file_type=file_type
        )
        for dep in dependency_file.resolved_dependencies:
            try:
                spec = next(iter(dep.specs))._spec
            except StopIteration:
                cls.LOGGER.info(
                    "Encountered StopIteration from Generator while parsing packages"  # noqa
                )
                continue

            version = spec[1]
            if spec[0] == "==":
                yield Package(
                    name=dep.name,
                    version=version,
                    insecure_versions=[],
                    secure_versions=[],
                    latest_version=None,
                    latest_version_without_known_vulnerabilities=None,
                    more_info_url=None,
                )
