"""
# Applescript

A package dealing with:
    - loading in AppleScript file paths from a config file
    - Running raw AppleScript code and AppleScript scripts
"""
from .script import load, run_code, run_script

FILE_EXTENSION = ".scpt"

__all__ = [
    "FILE_EXTENSION",
    "load",
    "run_code",
    "run_script",
]
