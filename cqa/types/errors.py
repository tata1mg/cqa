from enum import Enum
from typing import List, Optional, TypeVar

from cqa.config import constants

Self = TypeVar("Self", bound="ReporterError")


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ReporterError:
    """
    base class for reporting any errors
    """

    def __init__(
        self,
        path: str = "",
        message: str = "",
        col: int = 0,
        lnum: int = 0,
        strict: bool = False,
        severity: Severity = Severity.ERROR,
        **extras,
    ):
        self.path = path
        self.message = message
        self.col = col
        self.lnum = lnum
        self._strict = strict
        self.severity = severity
        self.details = extras

    def __repr__(self):
        return f"{self.path}:{self.lnum}:{self.col} - {self.message}"

    def __eq__(self, other: Self) -> bool:
        eq_path_and_message = (
            other.path == self.path and other.message == self.message
        )  # noqa

        # if strict check for col and lnum as well
        if self._strict:
            eq_col_and_lno = other.col == self.col and other.lnum == self.lnum
            return eq_col_and_lno and eq_path_and_message

        # otherwise only check for path and error message
        return eq_path_and_message


class PackageVulnerability:
    __cvssv2_score_severity = {
        3.9: Severity.WARNING,  # Low
        6.9: Severity.WARNING,  # Medium
        10: Severity.ERROR,  # High
    }

    __cvssv3_score_severity = {
        3.9: Severity.WARNING,  # Low
        6.9: Severity.WARNING,  # Medium
        8.9: Severity.ERROR,  # High
        10: Severity.ERROR,  # Critical
    }

    def __init__(
        self,
        vulnerability_id: str,
        package_name: str,
        current_version: str,
        advisory: str = "",
        cvssv2_score: Optional[int] = None,
        cvssv3_score: Optional[int] = None,
        affected_versions: List = [],
        more_info_url: Optional[str] = None,
    ):
        self.vulnerability_id = vulnerability_id
        self.package_name = package_name
        self.current_version = current_version
        self.affected_versions = affected_versions
        self.advisory = advisory
        self.more_info_url = more_info_url

        self.severity = Severity.WARNING
        if cvssv3_score:
            self.severity = self.__cvssv3_score_severity.get(
                next(
                    k for k in self.__cvssv3_score_severity if k > cvssv3_score
                )  # noqa
            )
        if not cvssv3_score and cvssv2_score:
            self.severity = self.__cvssv2_score_severity.get(
                next(
                    k for k in self.__cvssv2_score_severity if k > cvssv2_score
                )  # noqa
            )

        self.message = constants.VULNERABILITY_MSG_FORMAT.format(
            vulnerability_id=self.vulnerability_id,
            package_name=self.package_name,
            current_version=self.current_version,
            affected_versions=", ".join(self.affected_versions),
            advisory=self.advisory,
            severity=self.severity,
            more_info_url=self.more_info_url,
        )

    def __repr__(self):
        return self.message
