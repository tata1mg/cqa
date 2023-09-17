import subprocess
from typing import List


def get_output(command: List[str]) -> str:
    """
    run a command and return raw output

    :param command: (str) the command to run
    :returns: the stdout output of the command
    """
    result = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    return result.stdout.decode()


def get_lines(command: List[str]) -> List[str]:
    """
    run a command and return lines of output

    :param command: (str) the command to run
    :returns: list of whitespace-stripped lines output by command
    """
    stdout = get_output(command)
    return [line.strip() for line in stdout.splitlines()]
