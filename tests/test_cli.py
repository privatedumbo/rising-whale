"""Tests for `rising_whale`.cli module."""

from typing import List

import pytest
from typer.testing import CliRunner

import rising_whale
from rising_whale import cli

runner = CliRunner()


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "rising_whale.cli.main"),
        (["--help"], "Usage: "),
        (
            ["--version"],
            f"rising-whale, version { rising_whale.__version__ }\n",
        ),
    ],
)
def test_command_line_interface(options: List[str], expected: str) -> None:
    """Test the CLI."""
    result = runner.invoke(cli.app, options)
    assert result.exit_code == 0
    assert expected in result.stdout
