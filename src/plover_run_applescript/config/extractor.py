"""
Module to handle extracting data from data sources
"""

from typing import (
    Any,
    Tuple
)

from PyXA import AppleScript

from .. import (
    applescript,
    path
)


def load_applescripts(applescript_filepaths: list[str]) -> dict[str, Any]:
    """
    Loads applescripts from a set of filepaths
    """
    expanded_applescript_filepaths: list[Tuple[str, str]] = (
        path.expand_list(applescript_filepaths)
    )
    applescripts: dict[str, AppleScript] = {}

    for (filepath, expanded_filepath) in expanded_applescript_filepaths:
        try:
            applescripts[filepath] = applescript.load(expanded_filepath)
        except ValueError:
            # Ignore bad file paths and remove them from the set
            continue

    return applescripts
