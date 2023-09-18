import logging
from typing import Any, Dict, List

from cqa.types import ReporterError


class _RunnerLoggerMeta(type):
    def __init__(cls, name, bases, annotations, *args, **kwargs):
        # set ``LOGGER`` attribute
        setattr(cls, "LOGGER", logging.getLogger(cls.__name__))
        super().__init__(name, bases, annotations, *args, **kwargs)


class Runner(metaclass=_RunnerLoggerMeta):
    """
    base class for all runners
    """

    LOGGER: logging.Logger = None

    def get_config(self, cfg: Dict[str, Any]):
        """
        Abstract method to fetch and parse config parse from pyproject.toml data
        """

    def run(self, paths: List[str], rootdir: str) -> List[ReporterError]:
        """
        Abstract runner method to be overriden by sub-classes
        """
        raise NotImplementedError(
            f"run method is not implemented in {self.__class__.__name__}"
        )
