"""
Module to handle reading in the application JSON config file.
"""

from pathlib import Path
from typing import Any

from . import (
    extractor,
    file,
    transformer
)


def load(config_filepath: Path) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    data: dict[str, Any] = file.load(config_filepath) # extractor function
    applescript_filepaths: list[str] = transformer.transform_inbound(data)

    if not applescript_filepaths:
        return {}

    applescripts: dict[str, Any] = (
        extractor.load_applescripts(applescript_filepaths)
    )
    _save_any_changes(config_filepath, applescript_filepaths, applescripts)

    return applescripts

def save(config_filepath: Path, applescript_filepaths: list[str]) -> None:
    """
    Saves the set of applescript filepaths to the config JSON file.
    """
    data: dict[str, list[str]] = (
        transformer.transform_outbound(applescript_filepaths)
    )
    file.save(config_filepath, data)

def _save_any_changes(
    config_filepath: Path,
    applescript_filepaths: list[str],
    applescripts: dict[str, Any]
) -> None:
    sorted_applescript_filepaths: list[str] = sorted(applescripts.keys())

    if sorted_applescript_filepaths != applescript_filepaths:
        save(config_filepath, sorted_applescript_filepaths)
