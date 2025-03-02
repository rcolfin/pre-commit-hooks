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
EXECUTABLE_PATH: Final[str | None] = shutil.which("uv")
CMDS: Final[dict[str, tuple[str, ...]]] = {"check": ("lock", "--check"), "lock": ("lock",)}


def _get_changed_packages(filenames: Sequence[str]) -> set[Path]:
    changed_python_packages = util.changed_python_packages()
    changed_python_packages.update(util.changed_python_packages(util.changed_directories(map(Path, filenames))))
    return changed_python_packages


def main() -> int:
    parser = argparse.ArgumentParser()

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    common_parser.add_argument(
        "--cwd",
        type=str,
        default=str(Path.cwd()),
        help="The current working directory.",
    )
    subparsers = parser.add_subparsers(dest="cmd")
    for cmd in CMDS:
        subparsers.add_parser(cmd, help=f"Runs uv {cmd}", parents=[common_parser])

    args, extra_args = parser.parse_known_args()
    if EXECUTABLE_PATH is None:
        logger.error("uv not found.")
        return 1

    cmd = args.cmd
    cwd = Path(args.cwd)
    if not cwd.is_dir():
        logger.error("%s is not a directory.", cwd)
        return 1

    os.chdir(str(cwd))
    packages = _get_changed_packages(args.filenames)

    exitcode = 0
    for package in packages:
        native_cmds = CMDS[cmd]
        cmds = (EXECUTABLE_PATH, "--project", str(package), *native_cmds, *extra_args)
        logger.info(" ".join(cmds))
        retcode = subprocess.call(cmds, cwd=str(package))  # noqa: S603
        if retcode:
            exitcode = 1

    return exitcode


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    raise SystemExit(main())
