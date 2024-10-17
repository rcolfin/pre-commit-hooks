from pathlib import Path
from typing import Final

import pytest

from pre_commit_hooks import util

ROOT_PATH: Final[Path] = Path(__file__).parent.parent
NON_UNICODE_BYTES: Final[bytes] = b"\x89P"
SHEBANG_FMTS: Final[tuple[str, ...]] = ("#!/bin/{}", "#!/usr/bin/{}", "#!/bin/env {}", "#!/usr/bin/env {}")
UNSUPPORTED_SHELLS: Final[tuple[str, ...]] = ("python", "foo")


@pytest.fixture
def non_unicode_file(tmp_path: Path) -> Path:
    p = tmp_path / "non_unicode"
    p.write_bytes(NON_UNICODE_BYTES)
    return p


@pytest.fixture
def shebang_files(tmp_path: Path) -> list[Path]:
    return _create_shebang_files(tmp_path, util.SUPPORTED_SHELLS)


@pytest.fixture
def not_supported_shebang_files(tmp_path: Path) -> list[Path]:
    return _create_shebang_files(tmp_path, UNSUPPORTED_SHELLS)


def _create_shebang_files(tmp_path: Path, shells: tuple[str, ...]) -> list[Path]:
    files: list[Path] = []
    for shell in shells:
        for i, fmt in enumerate(SHEBANG_FMTS):
            p = tmp_path / f"{shell}.{i}"
            p.write_bytes(fmt.format(shell).encode())
            files.append(p)

    return files


@pytest.fixture
def files_with_supported_suffix(tmp_path: Path) -> list[Path]:
    files: list[Path] = []
    for suffix in util.SHELL_SCRIPT_SUFFIX:
        p = tmp_path / f"script.{suffix}"
        p.write_bytes(NON_UNICODE_BYTES)
        files.append(p)
    return files


def test_is_shell_script_on_shell_script_with_unsupported_shell_shebang(
    not_supported_shebang_files: list[Path],
) -> None:
    for shebang_file in not_supported_shebang_files:
        assert util.is_shell_script(shebang_file) is False, f"{shebang_file.read_text()}"


def test_is_shell_script_on_shell_script_with_supported_shell_shebang(shebang_files: list[Path]) -> None:
    for shebang_file in shebang_files:
        assert util.is_shell_script(shebang_file) is True, f"{shebang_file.read_text()}"


def test_is_shell_script_on_shell_script_with_file_ext(files_with_supported_suffix: list[Path]) -> None:
    for file in files_with_supported_suffix:
        assert util.is_shell_script(file) is True, f"{file} => {util.get_shell_interpreter(file)}"


def test_is_shell_script_on_yaml() -> None:
    assert util.is_shell_script(ROOT_PATH / "README.md") is False


def test_is_shell_script_on_non_unicode_file(non_unicode_file: Path) -> None:
    assert util.is_shell_script(non_unicode_file) is False
