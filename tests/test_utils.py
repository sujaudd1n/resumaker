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

# class TestGetConfig:
#     def test_when_load_config_raises_exception(self, mocker):
#         mocker.patch("resumaker.utils.load_config")
#         config = get_config()
#         assert type(config) == dict
#         assert len(config.keys()) == 1