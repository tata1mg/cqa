class Reporter:
    """
    abstract base class for all the reporters
    """

    def report(self, *_):
        raise NotImplementedError(
            f"method report not implemented for {self.__class__.__name__}"
        )
