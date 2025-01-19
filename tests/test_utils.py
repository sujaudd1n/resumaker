from resumaker.utils import *

import pytest
from pytest import MonkeyPatch
import os

@pytest.fixture
def delete_config_file():
    if os.path.exists("config.yml"):
        os.remove("config.yml")


@pytest.fixture
def create_invalid_config_file():
    open("config.yml", "w").close()
    yield
    os.remove("config.yml")


@pytest.fixture
def create_valid_config_file():
    f = open("config.yml", "w")
    f.write("key: value")
    f.close()
    yield
    os.remove("config.yml")



class TestLoadConfig:
    def test_config_file_does_not_exist(self, delete_config_file):
        config = load_config()
        assert config == ""

    def test_config_file_does_exist(self, delete_config_file):
        config = load_config()
        assert type(config) == str

    def test_get_invalid_user_config(self, mocker):
        mock = mocker.patch("resumaker.utils.get_rendered_config")
        mock.return_value = [None]

        with pytest.raises(ValueError) as excinfo:
            get_valid_user_config()
        assert excinfo.type is ValueError
        assert str(excinfo.value) == "config.yml is not valid!"

    def test_get_valid_user_config(self, mocker):
        mock = mocker.patch("resumaker.utils.get_rendered_config")
        mock.return_value = {"key": "value"}

        config = get_valid_user_config()
        assert config == {"key": "value"}

    def test_is_config_valid(self, create_invalid_config_file):
        config = None
        is_valid = is_config_valid(config)
        assert not is_valid

        config = {}
        is_valid = is_config_valid(config)
        assert is_valid

@pytest.fixture
def apply_default_configs():
    return default_configs

class TestGetConfig:
    def test_when_not_overwritten(self, apply_default_configs, mocker):
        mock = mocker.patch("resumaker.utils.get_valid_user_config")
        mock.return_value = {"key": "value"}
        config = get_config()
        assert config == default_configs

    def test_when_overwritten(self, apply_default_configs, mocker):
        mock = mocker.patch("resumaker.utils.get_valid_user_config")
        mock.return_value = {"RESUME_YAML_FILENAME": "custom_name.yml"}
        config = get_config()
        assert config == {"RESUME_YAML_FILENAME": "custom_name.yml"}

    def test_when_not_supported_config_are_given(self, apply_default_configs, mocker):
        mock = mocker.patch("resumaker.utils.get_valid_user_config")
        mock.return_value = {
            "RESUME_YAML_FILENAME": "custom_name.yml",
            "MY_CUSTOM_KEY": "MY_CUSTOM_VALUE",
        }
        config = get_config()
        assert config == {"RESUME_YAML_FILENAME": "custom_name.yml"}