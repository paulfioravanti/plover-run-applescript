import json
from pathlib import Path
import pytest


@pytest.fixture
def bad_config_path():
    return (Path(__file__).parent / "files/bad_json_data.json").resolve()

@pytest.fixture
def non_existent_config_path():
    return (Path(__file__).parent / "files/non_existent.json").resolve()

@pytest.fixture
def non_list_applescript_filepaths_config_path():
    return (
        Path(__file__).parent / "files/non_list_applescript_filepaths.json"
    ).resolve()

@pytest.fixture
def empty_list_applescript_filepaths_config_path():
    return (
        Path(__file__).parent / "files/empty_list_applescript_filepaths.json"
    ).resolve()

@pytest.fixture
def list_non_string_applescript_filepaths_config_path():
    return (
        Path(__file__).parent
        / "files/list_non_string_applescript_filepaths.json"
    ).resolve()

@pytest.fixture
def valid_applescript_filepaths_config_path():
    path = (
        Path(__file__).parent / "files/valid_applescript_filepaths.json"
    ).resolve()

    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()
