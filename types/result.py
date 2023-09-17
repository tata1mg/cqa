import itertools
from collections import defaultdict
from typing import List

from cqa.types import ReporterError, Severity


class Result:
    def __init__(self, errors: List[ReporterError]):
        groups = itertools.groupby(errors, key=lambda key: key.severity)

        _results = defaultdict(list)
        for sev, group in groups:
            _results[sev].extend(group)

        self._results = _results

    @property
    def errors(self):
        return self._results.get(Severity.ERROR, [])

    @property
    def warnings(self):
        return self._results.get(Severity.WARNING, [])

    @property
    def info(self):
        return self._results.get(Severity.INFO, [])
