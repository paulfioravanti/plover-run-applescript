import pytest
from pathlib import Path


@pytest.fixture
def non_existent_script_path():
    return _string_path("files/non-existent.scpt")

@pytest.fixture
def invalid_script_path():
    return _string_path("files/invalid.scpt")

@pytest.fixture
def valid_script_path():
    return _string_path("files/valid.scpt")

def _string_path(path):
    return str((Path(__file__).parent / path).resolve())
