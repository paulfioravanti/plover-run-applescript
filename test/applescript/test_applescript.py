import pytest

from PyXA import AppleScript

from plover_run_applescript import applescript

def test_loading_non_existent_script_filepath(non_existent_script_path):
    with pytest.raises(
        ValueError,
        match=f"Unable to load file from: {non_existent_script_path}"
    ):
        applescript.load(non_existent_script_path)

def test_loading_valid_script_filepath(valid_script_path):
    assert isinstance(applescript.load(valid_script_path), AppleScript)

def test_running_invalid_applescript_oneliner():
    with pytest.raises(
        ValueError,
        match=f"AppleScript code errored during execution"
    ):
        applescript.run_code("invalid")

def test_running_blank_applescript_oneliner():
    assert applescript.run_code("")["bool"] == False

def test_running_valid_applescript_oneliner():
    assert applescript.run_code("return true")["bool"] == True

def test_running_invalid_applescript_script(invalid_script_path):
    with pytest.raises(
        ValueError,
        match=f"AppleScript code errored during execution"
    ):
        script = applescript.load(invalid_script_path)
        applescript.run_script(script)

def test_running_valid_applescript_script(valid_script_path):
    script = applescript.load(valid_script_path)
    assert applescript.run_script(script)["bool"] == True
