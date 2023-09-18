import argparse


class Once(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(self, "seen", False):
            raise argparse.ArgumentError(
                self, "the argument can only be specified once"
            )
        setattr(self, "seen", True)
        setattr(namespace, self.dest, values)
