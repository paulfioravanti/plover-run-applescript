"""
Path - a module for dealing with expansion of ENV vars in a file path.
"""
import os
import re

_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL = "bash"
_INTERACTIVE_SHELLS = ["zsh", "bash"]

def expand_path(path: str) -> str:
    """
    Expands env vars in a file path.

    Raises an error if a value for the env var cannot be found.
    """
    shell = os.environ.get("SHELL", _DEFAULT_SHELL).split("/")[-1]
    # NOTE: Using an interactive mode command (bash/zsh -ci) seemed to be the
    # only way to access a user's env vars on their Mac outside Plover's
    # environment.
    flags = "-ci" if shell in _INTERACTIVE_SHELLS else "-c"
    parts = re.split(_ENV_VAR, path)
    expanded_parts = [_expand_path_part(part, shell, flags) for part in parts]
    return "".join(expanded_parts)

def _expand_path_part(part: str, shell: str, flags: str) -> str:
    if not part.startswith("$"):
        return part

    expanded = os.popen(f"{shell} {flags} 'echo {part}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {part}")

    return expanded
