"""
# Applescript

A package dealing with:
    - loading in AppleScript file paths from a config file
    - Running raw AppleScript code and AppleScript scripts
"""
from .script import load, run_code, run_script

__all__ = [
    "load",
    "run_code",
    "run_script",
]
