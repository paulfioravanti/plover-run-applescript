"""
Module to handle reading in the application JSON config file.
"""
import json
from pathlib import Path

from .. import applescript
from .. import path

def load(config_filepath: Path) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    try:
        with config_filepath.open(encoding="utf-8") as file:
            data = json.load(file)
            file.close()
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError as exc:
        raise ValueError("Config file must contain a JSON object") from exc

    config_applescript_filepaths = data.get("applescripts", [])
    if not isinstance(config_applescript_filepaths, list):
        raise ValueError("'applescripts' must be a list")

    applescripts = {}

    if not config_applescript_filepaths:
        return applescripts

    expanded_applescript_filepaths = list(zip(
        config_applescript_filepaths,
        path.expand_list(config_applescript_filepaths)
    ))
    for (filepath, expanded_filepath) in expanded_applescript_filepaths:
        try:
            applescripts[filepath] = applescript.load(expanded_filepath)
        except ValueError:
            # Ignore bad file paths and remove them from the set
            continue

    applescript_filepaths = sorted(applescripts.keys())

    if applescript_filepaths != config_applescript_filepaths:
        save(config_filepath, applescript_filepaths)

    return applescripts

def save(config_filepath: Path, applescript_filepaths: list[str]) -> None:
    """
    Saves the set of applescript filepaths to the config JSON file.
    """
    with config_filepath.open("w", encoding="utf-8") as file:
        json.dump({"applescripts": applescript_filepaths}, file, indent=2)
        file.close()
