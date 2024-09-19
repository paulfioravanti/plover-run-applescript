"""
Transformer

Module to handle transforming information from the application JSON config file
into a form the application can work with.
"""
from typing import Any

def transform(data: dict[str, Any]) -> list[str]:
    """
    Parse config data, providing defaults values where not provided.
    """
    filepaths: list[str] = data.get("applescripts", [])

    if (
        isinstance(filepaths, list)
        and all(isinstance(filepath, str) for filepath in filepaths)
    ):
        return filepaths

    raise TypeError("'applescripts' must be a list of strings")
