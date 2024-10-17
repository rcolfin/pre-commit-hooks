from __future__ import annotations

import logging
import re
import subprocess
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable


logger = logging.getLogger(__name__)
T = TypeVar("T")

SHELL_SCRIPT_SUFFIX: Final[tuple[str, ...]] = (".bash", ".dash", ".zsh", ".sh")
SUPPORTED_SHELLS: Final[tuple[str, ...]] = (
    "bash",
    "dash",
    "ksh",
    "sh",
)
SHEBANG_SHELL_PATTERN: Final[re.Pattern] = re.compile(
    rb"^#!\s*(?:\/bin\/env\s+|\/usr\/bin\/env\s+|\/bin\/|\/usr\/bin\/)?([^\s\/]+)"
)


class CalledProcessError(RuntimeError):
    pass


@cache
def _get_package_directories(pattern: str) -> list[Path]:
    """Gets the list of directories containing a pattern"""
    paths = [p.parent for p in Path.cwd().glob(pattern)]
    paths.sort(key=lambda x: -len(str(x.resolve())))
    return paths


def changed_files() -> set[Path]:
    """Gets the set of changed files."""
    cmd = ("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR")
    lines = cmd_output(*cmd).splitlines()
    return {Path(p) for p in lines}


def changed_directories(files: Iterable[Path] | None = None) -> set[Path]:
    """Gets the set of changed directories."""
    if files is None:
        files = changed_files()
    return {changed_file.parent for changed_file in files}


def changed_packages(pattern: str, directories: Iterable[Path] | None = None) -> set[Path]:
    """
    Gets the set of changed packages using the pattern to identify.

    Args:
        pattern (str): The search pattern to use to
            search in each of the changed_directories to identify a package.
        directories (Optional[Path]): The paths to search.

    Returns:
        set of paths.
    """
    if directories is None:
        directories = changed_directories()
    package_directories = _get_package_directories(pattern)
    return {p for p in package_directories if any(str(d.resolve()).startswith(str(p.resolve())) for d in directories)}


def changed_python_packages(directories: Iterable[Path] | None = None) -> set[Path]:
    """Gets the set of changed Python directories."""
    return changed_packages("**/pyproject.toml", directories)


def is_shell_script(file: Path) -> bool:
    """Determines if the file is a shell script"""
    if file.suffix.lower() in SHELL_SCRIPT_SUFFIX:
        return True

    return get_shell_interpreter(file) in SUPPORTED_SHELLS


def get_shell_interpreter(file: Path) -> str | None:
    with file.open("rb") as f:
        line = f.readline()
    m = SHEBANG_SHELL_PATTERN.match(line)
    if m is None:
        return None
    return m.groups()[0].decode()


def cmd_output(
    *cmd: str,
    retcode: int | None = 0,
    **kwargs: Any,  # noqa: ANN401
) -> str:
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    logger.debug("Running %s", " ".join(cmd))
    proc = subprocess.Popen(cmd, **kwargs)  # noqa: S603
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def flatten(lst_of_lsts: Iterable[Iterable[T]]) -> Iterable[T]:
    return (item for lst in lst_of_lsts for item in lst)
