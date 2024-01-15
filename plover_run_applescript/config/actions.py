"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import Any, Tuple

from .. import applescript
from .. import path
from . import file

def load(config_filepath: Path) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    data = file.load(config_filepath)
    config_applescript_filepaths = _parse(data)
    if not config_applescript_filepaths:
        return {}

    expanded_applescript_filepaths = path.expand_list(
        config_applescript_filepaths
    )
    applescripts = _load_applescripts(expanded_applescript_filepaths)
    _save_any_changes(
        config_filepath,
        config_applescript_filepaths,
        applescripts
    )

    return applescripts

def save(config_filepath: Path, applescript_filepaths: list[str]) -> None:
    """
    Saves the set of applescript filepaths to the config JSON file.
    """
    data = {"applescripts": applescript_filepaths}
    file.save(config_filepath, data)

def _parse(data: dict[str, Any]) -> list[str]:
    filepaths = data.get("applescripts", [])

    if not isinstance(filepaths, list):
        raise ValueError("'applescripts' must be a list")

    return filepaths

def _load_applescripts(
    expanded_applescript_filepaths: list[Tuple[str, str]]
) -> dict[str, Any]:
    applescripts = {}
    for (filepath, expanded_filepath) in expanded_applescript_filepaths:
        try:
            applescripts[filepath] = applescript.load(expanded_filepath)
        except ValueError:
            # Ignore bad file paths and remove them from the set
            continue

    return applescripts

def _save_any_changes(
    config_filepath: Path,
    config_applescript_filepaths: list[str],
    applescripts: dict[str, Any]
) -> None:
    applescript_filepaths = sorted(applescripts.keys())

    if applescript_filepaths != config_applescript_filepaths:
        save(config_filepath, applescript_filepaths)
