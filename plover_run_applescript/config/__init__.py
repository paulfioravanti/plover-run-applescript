"""
# Config

A package dealing with:
    - loading and saving config containing filepath pointers to compiled
      AppleScript files
"""
from .actions import load, save

__all__ = [
    "load",
    "save",
]
