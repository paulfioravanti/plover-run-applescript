"""
# Config

A package dealing with:
    - loading and saving config containing filepath pointers to compiled
      AppleScript files
"""

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save",
]

from .loader import (
    load,
    save
)


CONFIG_BASENAME: str = "run_applescript.json"
