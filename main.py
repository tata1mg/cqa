import logging
import os
import sys
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

import toml

from cqa import utils
from cqa.cli.args import get_args
from cqa.reporters.console import ConsoleReporter
from cqa.securitytools.base import SecurityTools, VulnerabilityRunner
from cqa.statictools.base import Formatter, Linter


def get_cqa_config(path: str):
    if not os.path.exists(path):
        logging.error("config file not found, using baseline config")
        return {}

    config = toml.load(path)
    return config.get("tool", {}).get("cqa", {})


def main():
    args = get_args()
    config = get_cqa_config(args.config)
    logging.basicConfig(level=logging.ERROR)

    if getattr(args, "action") != "run":
        if getattr(args, "install_git_hook", False):
            utils.install_git_hook()
            return

    with ThreadPoolExecutor(max_workers=4) as _executor:
        _linter_fut = _executor.submit(
            _get_linter_result, args, config.get("linter", {})
        )
        _formatter_fut = _executor.submit(
            _get_formatter_result, args, config.get("formatter", {})
        )
        _security_fut = _executor.submit(
            _get_secuirty_result, args, config.get("sec", {})
        )
        _vuln_fut = _executor.submit(
            _get_vulnerability_result, config.get("vuln", {})
        )

        _futures = [_linter_fut, _security_fut, _vuln_fut]
        if getattr(args, "format", False):  # If `format` is specified
            _futures.append(_formatter_fut)

        # Wait until all the coroutines are completed
        wait(_futures, return_when=ALL_COMPLETED)

        linter_result = _linter_fut.result()
        formatter_result = _formatter_fut.result()
        security_result = _security_fut.result()
        vuln_result = _vuln_fut.result()

    reporter = ConsoleReporter()
    reporter.report(linter_result, header="Formatting Issues")
    reporter.report(security_result, header="Security Issues")
    reporter.report(vuln_result, header="Vulnerability Issues")

    if getattr(args, "fail", False):
        if (
            linter_result.errors
            or formatter_result.errors
            or security_result.errors
            or vuln_result.errors
        ):
            logging.critical(
                "Could not create a commit as there \
                    are errors in your committed code"
            )
            sys.exit(1)


def _get_linter_result(args, config):
    linter = Linter(
        args.path,
        rootdir=os.getcwd(),
        options=config,
    )
    return linter.run()


def _get_formatter_result(args, config):
    formatter = Formatter(
        args.path,
        rootdir=os.getcwd(),
        options=config,
    )
    return formatter.run()


def _get_secuirty_result(args, config):
    securitytools = SecurityTools(
        args.path,
        rootdir=os.getcwd(),
        options=config,
    )
    return securitytools.run()


def _get_vulnerability_result(config):
    vulnerabilitytool = VulnerabilityRunner(config)
    return vulnerabilitytool.run()
