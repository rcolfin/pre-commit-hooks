from pathlib import Path
from typing import Final

import pytest

from pre_commit_hooks import util

ROOT_PATH: Final[Path] = Path(__file__).parent.parent
NON_UNICODE_BYTES: Final[bytes] = b"\x89P"


@pytest.fixture
def non_unicode_file(tmp_path: Path) -> Path:
    p = tmp_path / "non_unicode"
    p.write_bytes(NON_UNICODE_BYTES)
    return p


@pytest.fixture
def shebang_file(tmp_path: Path) -> Path:
    p = tmp_path / "script"
    p.write_bytes(b"#!")
    return p


@pytest.fixture
def sh_file_extension(tmp_path: Path) -> Path:
    p = tmp_path / "script.sh"
    p.write_bytes(NON_UNICODE_BYTES)
    return p


def test_is_shell_script_on_shell_script_with_shebang(shebang_file: Path) -> None:
    assert util.is_shell_script(shebang_file) is True


def test_is_shell_script_on_shell_script_with_file_ext(sh_file_extension: Path) -> None:
    assert util.is_shell_script(sh_file_extension) is True


def test_is_shell_script_on_yaml() -> None:
    assert util.is_shell_script(ROOT_PATH / "README.md") is False


def test_is_shell_script_on_non_unicode_file(non_unicode_file: Path) -> None:
    assert util.is_shell_script(non_unicode_file) is False
