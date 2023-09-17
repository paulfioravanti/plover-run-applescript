"""
Path - a module for dealing with expansion of ENV vars in a file path.
"""
import os
import re

_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")

def expand_path(path: str) -> str:
    """
    Expands env vars in a file path.

    Raises an error if a value for the env var cannot be found.
    """
    parts = re.split(_ENV_VAR, path)
    expanded_parts = [_expand_path_part(part) for part in parts]
    return "".join(expanded_parts)

def _expand_path_part(part: str) -> str:
    if not part.startswith("$"):
        return part

    # NOTE: Using os.popen with an interactive mode bash command
    # (bash -ci) seemed to be the only way to access a user's env
    # vars on their Mac outside Plover's environment.
    expanded = os.popen(f"bash -ci 'echo {part}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {part}")

    return expanded
