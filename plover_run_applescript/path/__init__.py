"""
# Path

A package dealing with:
    - expanding local environment variables within a filepath
"""
from .expand import expand, expand_list

__all__ = [
    "expand",
    "expand_list",
]
