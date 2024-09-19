"""
# Config

A package dealing with:
    - loading and saving config containing filepath pointers to compiled
      AppleScript files
"""
from .actions import (
    load,
    save
)


__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save",
]

CONFIG_BASENAME: str = "run_applescript.json"
