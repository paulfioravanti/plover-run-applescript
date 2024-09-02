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
from .file import CONFIG_BASENAME

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save",
]
