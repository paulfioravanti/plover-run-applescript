import json
from pathlib import Path
import pytest

from plover_run_applescript import config

# Files

@pytest.fixture
def bad_config_path():
    return (Path(__file__).parent / "files/bad_json_data.json").resolve()

@pytest.fixture
def non_existent_config_path():
    return (Path(__file__).parent / "files/non_existent.json").resolve()

@pytest.fixture
def non_array_applescript_filepaths_config_path():
    return (
        (
            Path(__file__).parent /
            "files/non_array_applescript_filepaths.json"
        ).resolve()
    )

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

# Tests

def test_bad_config(mocker, bad_config_path):
    with pytest.raises(
        ValueError,
        match="Config file must contain a JSON object"
    ):
        config.load(bad_config_path)

def test_non_existent_config(non_existent_config_path):
    loaded_config = config.load(non_existent_config_path)
    assert loaded_config == {}

def test_config_with_non_array_applescript_filepaths_names(
    non_array_applescript_filepaths_config_path
):
    with pytest.raises(ValueError, match="'applescripts' must be a list"):
        config.load(non_array_applescript_filepaths_config_path)

def test_loading_existing_applescripts(
    mocker,
    valid_applescript_filepaths_config_path
):
    def filepath_switch(filepath):
        if filepath == "path/to/foo.scpt":
          return "foo.scpt contents"
        elif filepath == "path/to/bar.scpt":
          return "bar.scpt contents"

    filepath_mock = mocker.Mock(side_effect=filepath_switch)
    mocker.patch("plover_run_applescript.applescript.load", filepath_mock)
    loaded_config = config.load(valid_applescript_filepaths_config_path)
    assert loaded_config == {
        "path/to/foo.scpt": "foo.scpt contents",
        "path/to/bar.scpt": "bar.scpt contents",
    }

    # No change to original config file
    with valid_applescript_filepaths_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_applescript_filepaths = data.get("applescripts", [])
    assert config_applescript_filepaths == [
        "path/to/bar.scpt", "path/to/foo.scpt"
    ]

def test_loading_non_existent_applescript_filepaths(
    valid_applescript_filepaths_config_path
):
    loaded_config = config.load(valid_applescript_filepaths_config_path)
    assert loaded_config == {}

    # Original config file has been blanked out
    with valid_applescript_filepaths_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("applescripts", [])
    assert config_env_var_names == []

def test_loading_some_existing_applescript_filepaths(
    mocker,
    valid_applescript_filepaths_config_path
):
    def filepath_switch(filepath):
        if filepath == "path/to/foo.scpt":
          return "foo.scpt contents"
        else:
          raise ValueError

    filepath_mock = mocker.Mock(side_effect=filepath_switch)
    mocker.patch("plover_run_applescript.applescript.load", filepath_mock)

    loaded_config = config.load(valid_applescript_filepaths_config_path)
    assert loaded_config == {
        "path/to/foo.scpt": "foo.scpt contents",
    }

    # Original config file has had invalid bar.scpt path removed from it
    with valid_applescript_filepaths_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_applescript_filepaths = data.get("applescripts", [])
    assert config_applescript_filepaths == [
        "path/to/foo.scpt"
    ]
