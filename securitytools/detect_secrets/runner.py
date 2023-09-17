from typing import List

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings

from cqa.types import ReporterError, Severity


class DetectSecretsRunner:

    _collection = SecretsCollection()

    @classmethod
    def run(cls, paths: List[str], _rootdir: str):
        with default_settings():
            cls._collection.scan_files(*paths)

        result = []
        for path, issues in cls._collection.data.items():
            result.extend(
                [
                    ReporterError(
                        path=path,
                        message=issue.type,
                        lnum=issue.line_number,
                        severity=Severity.WARNING,
                    )
                    for issue in issues
                ]
            )

        return result
