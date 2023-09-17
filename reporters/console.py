import itertools
from typing import List, Union

import rich
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.theme import Theme

from cqa.reporters.base import Reporter
from cqa.types import PackageVulnerability, ReporterError, Result


class ConsoleReporter(Reporter):

    custom_theme = Theme(
        {"info": "dim cyan", "warning": "yellow", "error": "bold red"},
    )

    def report(self, result: Result, header=None):
        console = Console(theme=self.custom_theme)

        rich.print(Panel(header, title_align="center"))

        self._report_helper(
            console,
            result.errors,
            header="Errors",
        )

        self._report_helper(
            console,
            result.warnings,
            header="Warnings",
        )

        console.print("\n")

    def _report_helper(
        self,
        console: Console,
        items: List[Union[ReporterError, PackageVulnerability]],
        header=None,
    ):

        if items:
            if isinstance(items[0], PackageVulnerability):
                self._report_vulns(console, items, header)
            else:
                self._report_reporter_error(console, items, header)

    def _report_reporter_error(
        self, console: Console, items: List[ReporterError], header=None
    ):
        filegroups = itertools.groupby(items, key=lambda key: key.path)

        if header is not None and items:
            console.rule(header, style="bold rule.line")

        for path, group in filegroups:
            linegroups = itertools.groupby(group, key=lambda key: key.lnum)
            console.rule(path)
            for lnum, group in linegroups:
                for err in group:
                    console.print(
                        f"{err.lnum}:{err.col} {err.message}",
                        style=err.severity.value,
                    )
                console.print(
                    Syntax.from_path(
                        path,
                        line_numbers=True,
                        line_range=(lnum - 1, lnum + 1),
                        highlight_lines=[lnum],
                    ),
                )

    def _report_vulns(
        self, console: Console, items: List[PackageVulnerability], header=None
    ):
        if header is not None and items:
            console.rule(header, style="bold rule.line")

        for item in items:
            console.print(item, style=item.severity.value)
