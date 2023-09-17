ISORT_ERROR_MSG = "Incorrectly sorted imports"
TYPE_MISMATCH_ERROR = "Type annotation does not match of assignment"

LOG_FORMAT = "%(asctime)s %(levelname)-4s %(message)s"
VULNERABILITY_MSG_FORMAT = """
{severity} Vulnerability found in {package_name}=={current_version}; \
Versions affected: {affected_versions}
{advisory}
Get more info: {more_info_url}
"""
FILE_FORMATTED_ERROR = "File {path} does not satisfy the given configuration, modifying using {linter}.."  # noqa
