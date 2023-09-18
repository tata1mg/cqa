import asyncio
import functools
import itertools
import sys
from typing import Dict, List, Optional

import aiofiles
from pytype import analyze, config, load_pytd

from cqa.base import Runner
from cqa.config import constants
from cqa.types import ReporterError, Severity

WARNINGS = frozenset(["annotation-type-mismatch"])
ERRORS = frozenset(["unsupported-operands", "wrong-arg-types"])
ERROR_MAPPING = {
    Severity.WARNING: WARNINGS,
    Severity.ERROR: ERRORS,
}


class PytypeRunner(Runner):
    _options = {
        "python_version": sys.version_info[:2],
        "enable_cached_property": True,
        "overriding_parameter_count_checks": True,
        "overriding_return_type_checks": True,
        "strict_parameter_checks": True,
        "strict_primitive_comparisons": True,
        "use_enum_overlay": True,
    }
    _loader = None
    _opt = None

    def __init__(self, options: Optional[Dict] = None):
        if options is None:
            options = {}

        # override pytype options with newer options
        self._options.update(options)
        self._opt = config.Options.create(**self._options)
        self._loader = load_pytd.create_loader(self._opt)

    @property
    @functools.lru_cache()
    def __REVERSE_ERROR_MAPPING(self) -> Dict:
        REVERSE_MAPPING = {}
        for k, v in ERROR_MAPPING.items():
            for name in v:
                REVERSE_MAPPING[name] = k
        return REVERSE_MAPPING

    def run(self, paths: List[str], rootdir: str) -> List[ReporterError]:
        coro = []  # List of all the coroutines
        for filename in paths:
            coro.append(self._run_for_single_path(filename))

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        futures = asyncio.gather(*coro)
        errors = event_loop.run_until_complete(futures)
        event_loop.close()
        return list(itertools.chain.from_iterable(errors))

    async def _run_for_single_path(self, path) -> List[ReporterError]:
        errors: List[ReporterError] = []
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            src = await f.read()
            ret = analyze.check_types(
                src=src,
                filename=path,
                options=self._opt,
                loader=self._loader,
            )

            for error in ret.errorlog:
                error_name = getattr(error, "_name")
                if error_name in WARNINGS | ERRORS:
                    message = getattr(
                        error,
                        "_message",
                        constants.TYPE_MISMATCH_ERROR,
                    )
                    severity = self.__REVERSE_ERROR_MAPPING.get(
                        error_name, Severity.WARNING
                    )
                    errors.append(
                        ReporterError(
                            path=path,
                            message=message,
                            lnum=getattr(error, "_lineno", 0),
                            severity=severity,
                        )
                    )

        return errors
