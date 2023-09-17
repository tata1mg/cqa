import inspect
from types import ModuleType
from typing import List

from cqa.types import Function


def find_callables(module: ModuleType) -> List[Function]:
    """
    Function to find all the callable methods in the given module

    :param module: (ModuleType) Module where to find the callables
    """
    callables: List[callable] = []

    for name, method in inspect.getmembers(module):
        if callable(getattr(module, name)):
            callables.append(method)

    methods: List[Function] = []
    for method in callables:
        args = inspect.getargs(method)
        name = getattr(method, "__name__", repr(method))

        methods.append(Function(name=name, args=args))

    return methods
