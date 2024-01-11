"""
Path - a module for dealing with expansion of ENV vars in a file path.
"""
import os
import re

from typing import Tuple


_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL = "bash"
_INTERACTIVE_SHELLS = ["zsh", "bash"]
_VAR_DIVIDER = "##"
_ENV_VAR_SYNTAX = "$"

def expand(path: str) -> str:
    """
    Expands env vars in a file path.

    Raises an error if a value for the env var cannot be found.
    """
    parts = re.split(_ENV_VAR, path)
    (shell, flags) = _fetch_shell_and_flags()
    expanded_parts = []
    for part in parts:
        if part.startswith(_ENV_VAR_SYNTAX):
            expanded_parts.append(_perform_expansion(part, shell, flags))
        else:
            expanded_parts.append(part)

    return "".join(expanded_parts)

def expand_list(filepath_list: list[str]) -> list[str]:
    """
    Returns a list of expanded filepaths from a list of filepaths.

    Removes a filepath from the list if its value is blank.
    """
    filepaths = _VAR_DIVIDER.join(filepath_list)
    (shell, flags) = _fetch_shell_and_flags()
    expanded = _perform_expansion(filepaths, shell, flags)

    return expanded.split(_VAR_DIVIDER)

def _fetch_shell_and_flags() -> Tuple[str, str]:
    shell = os.environ.get("SHELL", _DEFAULT_SHELL).split("/")[-1]
    # NOTE: Using an interactive mode command (bash/zsh -ci) seemed to be the
    # only way to access a user's env vars on a Mac outside Plover's
    # environment.
    flags = "-ci" if shell in _INTERACTIVE_SHELLS else "-c"
    return (shell, flags)

def _perform_expansion(target: str, shell: str, flags: str) -> str:
    expanded = os.popen(f"{shell} {flags} 'echo {target}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {target}")

    return expanded
