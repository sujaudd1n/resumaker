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


@pytest.fixture
def create_valid_config_file():
    f = open("config.yml", "w")
    f.write("key: value")
    f.close()


def test_config_file_does_not_exist(delete_config_file):
    config = load_config()
    assert config == {}


def test_config_file_exists_but_invalid(create_invalid_config_file):
    with pytest.raises(SystemExit) as exc:
        load_config()
    assert str(exc.value) == "config.yml is not valid."


def test_config_file_exists_and_valid(create_valid_config_file):
    config = load_config()
    assert type(config) == dict
