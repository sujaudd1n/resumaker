from resumaker.utils import load_config, get_config

import pytest
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
    def test_config_file_does_not_exist(self):
        with pytest.raises(FileNotFoundError):
            load_config()


    def test_config_file_exists_but_invalid(self, create_invalid_config_file):
        with pytest.raises(ValueError) as excinfo:
            load_config()
        assert excinfo.type is ValueError
        assert str(excinfo.value) == "config.yml is not valid."


    def test_config_file_exists_and_valid(self, create_valid_config_file):
        config = load_config()
        assert type(config) == dict

class TestGetConfig:
    # def test_when
    pass