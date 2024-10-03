"""
Transformer

Module to handle transforming information from the application JSON config file
into a form the application can work with.
"""

from typing import Any

def transform_inbound(data: dict[str, Any]) -> list[str]:
    """
    Transform inbound config data, providing defaults values where not provided.
    """
    filepaths: list[str] = data.get("applescripts", [])

    if (
        isinstance(filepaths, list)
        and all(isinstance(filepath, str) for filepath in filepaths)
    ):
        return filepaths

    raise TypeError("'applescripts' must be a list of strings")

def transform_outbound(filepaths: list[str]) -> dict[str, list[str]]:
    """
    Transform filepaths into outbound config data.
    """
    return {"applescripts": filepaths}
