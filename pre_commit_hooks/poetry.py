from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Final

from pre_commit_hooks import util

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)
POETRY_PATH: Final[str | None] = shutil.which("poetry")
POETRY_CMDS: Final[tuple[str, ...]] = ("check", "lock")


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
    subparsers = parser.add_subparsers(dest="cmd")
    for cmd in POETRY_CMDS:
        subparsers.add_parser(cmd, help=f"Runs poetry {cmd}", parents=[common_parser])

    args, extra_args = parser.parse_known_args()
    if POETRY_PATH is None:
        logger.error("poetry not found.")
        return 1

    cmd = args.cmd
    packages = _get_changed_packages(args.filenames)

    exitcode = 0
    for package in packages:
        cmds = (POETRY_PATH, "-C", str(package), cmd, *extra_args)
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
