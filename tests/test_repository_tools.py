from pathlib import Path

import pytest

from app.tools.repository import (
    list_files,
    read_file,
    search_code,
)

def test_list_files_returns_repository_files(
    tmp_path: Path,
) -> None:
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "# Test",
        encoding="utf-8",
    )

    result = list_files(str(tmp_path))

    assert result == [
        "README.md",
        "app/main.py",
    ]


def test_list_files_ignores_hidden_project_directories(
    tmp_path: Path,
) -> None:
    cache_dir = tmp_path / "__pycache__"
    cache_dir.mkdir()

    (cache_dir / "main.pyc").write_text(
        "ignored",
        encoding="utf-8",
    )
    (tmp_path / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    result = list_files(str(tmp_path))

    assert result == ["main.py"]


def test_list_files_raises_error_for_missing_path() -> None:
    with pytest.raises(FileNotFoundError):
        list_files("/path/that/does/not/exist")



def test_read_file_returns_content(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "main.py"

    file_path.write_text(
        "print('hello')",
        encoding="utf-8",
    )

    result = read_file(
        str(tmp_path),
        "main.py",
    )

    assert result == "print('hello')"




def test_read_file_raises_error_for_missing_file(
    tmp_path: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        read_file(
            str(tmp_path),
            "missing.py",
        )



def test_read_file_blocks_path_traversal(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError):
        read_file(
            str(tmp_path),
            "../secret.txt",
        )        


def test_search_code_finds_matching_lines(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "main.py"

    file_path.write_text(
        "from fastapi import FastAPI\n"
        "app = FastAPI()\n",
        encoding="utf-8",
    )

    result = search_code(
        str(tmp_path),
        "FastAPI",
    )

    assert result == [
        "main.py:1: from fastapi import FastAPI",
        "main.py:2: app = FastAPI()",
    ]





def test_search_code_is_case_insensitive(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "main.py"

    file_path.write_text(
        "FastAPI application",
        encoding="utf-8",
    )

    result = search_code(
        str(tmp_path),
        "fastapi",
    )

    assert result == [
        "main.py:1: FastAPI application"
    ]


def test_search_code_respects_max_results(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "main.py"

    file_path.write_text(
        "error\n"
        "error\n"
        "error\n",
        encoding="utf-8",
    )

    result = search_code(
        str(tmp_path),
        "error",
        max_results=2,
    )

    assert len(result) == 2                