import pytest


@pytest.fixture
def path_without_env_vars():
    return "/Users/test_user/some_directory"

@pytest.fixture
def path_with_env_var():
    return "$HOME/some_directory"

@pytest.fixture
def path_with_multiple_env_vars(path_with_env_var):
    return path_with_env_var + "/$STENO_DICTIONARIES"
