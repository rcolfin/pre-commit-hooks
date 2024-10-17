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

SHELLCHECK_PATH: Final[str | None] = shutil.which("shellcheck")


def _get_files(filenames: Sequence[str]) -> set[Path]:
    changed_files = {p.resolve() for p in util.changed_files()}
    changed_files.update(Path(p).resolve() for p in filenames)
    return changed_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )

    args, extra_args = parser.parse_known_args()

    if SHELLCHECK_PATH is None:
        logger.error("shellcheck not found.")
        return 1

    files = _get_files(args.filenames)
    cwd = Path.cwd().resolve()

    exitcode = 0
    cmds = ("shellcheck", *extra_args)
    for file in files:
        if not util.is_shell_script(file):
            logger.debug("%s is not a shell script.", file.relative_to(cwd))
            continue

        pcmd = (*cmds, str(file))
        logger.info(" ".join(pcmd))
        retcode = subprocess.call(pcmd)  # noqa: S603
        if retcode:
            exitcode = 1

    return exitcode


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    raise SystemExit(main())
