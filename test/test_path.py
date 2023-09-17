import os
import pytest

from plover_run_applescript import path


@pytest.fixture
def path_without_env_vars():
    return "/Users/test_user/some_directory"

@pytest.fixture
def path_with_env_var():
    return "$HOME/some_directory"

@pytest.fixture
def path_with_multiple_env_vars(path_with_env_var):
    return path_with_env_var + "/$STENO_DICTIONARIES"

def test_no_env_vars_in_path(path_without_env_vars):
    assert path.expand_path(path_without_env_vars) == path_without_env_vars

def test_one_undefined_env_var_in_path(monkeypatch, path_with_env_var):
    monkeypatch.setenv("HOME", "")

    with pytest.raises(ValueError, match="No value found for env var: \\$HOME"):
        path.expand_path(path_with_env_var)

def test_one_defined_env_var_in_path(monkeypatch, path_with_env_var):
    monkeypatch.setenv("HOME", "/Users/env_var_user")

    assert (
        path.expand_path(path_with_env_var)
        == "/Users/env_var_user/some_directory"
    )

def test_multiple_defined_env_vars_in_path(
    monkeypatch,
    path_with_multiple_env_vars
):
    monkeypatch.setenv("HOME", "/Users/env_var_user")
    monkeypatch.setenv("STENO_DICTIONARIES", "dictionaries_path")

    assert (
        path.expand_path(path_with_multiple_env_vars)
        == "/Users/env_var_user/some_directory/dictionaries_path"
    )

def test_multiple_env_vars_in_path_with_one_defined_and_one_undefined(
    monkeypatch,
    path_with_multiple_env_vars
):
    monkeypatch.setenv("HOME", "/Users/env_var_user")
    monkeypatch.setenv("STENO_DICTIONARIES", "")

    with pytest.raises(
        ValueError,
        match="No value found for env var: \\$STENO_DICTIONARIES"
    ):
        path.expand_path(path_with_multiple_env_vars)
