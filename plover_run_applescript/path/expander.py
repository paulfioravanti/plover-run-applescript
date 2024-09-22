"""
Expander - a module for dealing with expansion of ENV vars in a file path.
"""

import os
import re
from typing import (
    Pattern,
    Tuple
)


_ENV_VAR: Pattern[str] = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
# NOTE: Entire shell path cannot be used because Plover's shell location may
# not be the same as the user's machine.
_SHELL: str = os.getenv("SHELL", "bash").split("/")[-1]
_VAR_DIVIDER: str = "##"
_ENV_VAR_SYNTAX: str = "$"

def expand(path: str) -> str:
    """
    Expands env vars in a file path.

    Raises an error if a value for the env var cannot be found.
    """
    parts: list[str] = re.split(_ENV_VAR, path)
    expanded_parts: list[str] = []

    for part in parts:
        if part.startswith(_ENV_VAR_SYNTAX):
            expanded_parts.append(_perform_expansion(part))
        else:
            expanded_parts.append(part)

    return "".join(expanded_parts)

def expand_list(filepath_list: list[str]) -> list[Tuple[str, str]]:
    """
    Returns a list of expanded filepaths from a list of filepaths.

    Removes a filepath from the list if its value is blank.
    """
    filepaths: str = _VAR_DIVIDER.join(filepath_list)
    expanded_filepaths: str = _perform_expansion(filepaths)
    expanded_filepath_list: list[Tuple[str, str]] = (
        list(zip(filepath_list, expanded_filepaths.split(_VAR_DIVIDER)))
    )

    return expanded_filepath_list

def _perform_expansion(target: str) -> str:
    # NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
    # the only way to access a user's env vars on a Mac outside Plover's
    # environment.
    expanded: str = os.popen(f"{_SHELL} -ic 'echo {target}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {target}")

    return expanded
