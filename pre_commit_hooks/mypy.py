from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Final

from pre_commit_hooks import util

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)
EXECUTABLES: Final[list[str]] = ["poetry", "uv"]
EXECUTABLE_PATHS: Final[list[str | None]] = [shutil.which(x) for x in EXECUTABLES]


def _get_changed_packages(filenames: Sequence[str]) -> set[Path]:
    changed_python_packages = util.changed_python_packages()
    changed_python_packages.update(util.changed_python_packages(util.changed_directories(map(Path, filenames))))
    return changed_python_packages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=str(Path.cwd()),
        help="The current working directory.",
    )

    args, extra_args = parser.parse_known_args()
    executable = next((ex for ex in EXECUTABLE_PATHS if ex), None)
    if not executable:
        logger.error("unable to locate either poetry or uv.")
        return 1

    cwd = Path(args.cwd).resolve()
    if not cwd.is_dir():
        logger.error("%s is not a directory.", cwd)
        return 1

    os.chdir(str(cwd))
    packages = _get_changed_packages(args.filenames)

    exitcode = 0
    cmds = (executable, "run", "mypy", *extra_args)
    for package in packages:
        pcmd = (*cmds, str(package))
        retcode = subprocess.call(pcmd, cwd=str(package))  # noqa: S603
        if retcode:
            exitcode = 1

    return exitcode


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    raise SystemExit(main())
