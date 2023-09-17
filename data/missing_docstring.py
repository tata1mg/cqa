"""
This module is to run the test if the given class module
contains a valid docstring or not
"""


class NoDocstring:
    def docstring_func(self):
        """
        this function contains a docstring but does nothing
        """
        pass

    def no_docstring_func(self):
        pass
