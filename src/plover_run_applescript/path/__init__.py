"""
# Path

A package dealing with:
    - expanding local environment variables within a filepath
"""

__all__ = [
    "expand",
    "expand_list",
]

from .expander import (
    expand,
    expand_list
)
