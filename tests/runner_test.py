from pathlib import Path
from typing import Any, Callable
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

import runner as R


@pytest.fixture()
def mocked_run_check(monkeypatch: pytest.MonkeyPatch) -> Callable[..., None]:
    monkeypatch.setattr(R, "_run", mock := MagicMock())

    def check(*args: Any) -> None:
        mock.assert_called_once_with(*args)

    return check


def test_defaults(mocked_run_check: Callable[..., None]) -> None:
    _run_check(["1"])
    mocked_run_check(1, 1, None)


@pytest.mark.parametrize("full", (True, False))
def test_valid(
    mocked_run_check: Callable[..., None], full: bool, tmp_path: Path
) -> None:
    tmp_file = tmp_path / "baz"
    tmp_file.touch()
    _run_check(["15", "2", "--file" if full else "-f", str(tmp_file)])
    mocked_run_check(15, 2, tmp_file)


@pytest.mark.parametrize(
    "cases, msg",
    [
        ((0, 1, None), "Invalid value for 'DAY'"),
        ((30, 1, None), "Invalid value for 'DAY'"),
        ((3, 3, None), "Invalid value for '[VAR]'"),
        ((3, 0, None), "Invalid value for '[VAR]'"),
        ((1, 1, "-f", "foo"), "File 'foo' does not exist"),
        ((1, 1, "-f", "."), "File '.' is a directory"),
    ],
)
def test_invalid(cases: tuple[Any, ...], msg: str):
    runner = CliRunner()
    args = [str(x) for x in cases]
    res = runner.invoke(R.run, args)
    assert res.exit_code == 2
    assert msg in res.stdout


def _run_check(args: list[str]) -> None:
    runner = CliRunner()
    res = runner.invoke(R.run, args)
    assert res.exit_code == 0, res.stdout
