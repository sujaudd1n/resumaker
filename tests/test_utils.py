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


class TestGetConfig:
    def test_when_filenotfound(self, mocker):
        mocked_load_config = mocker.patch("resumaker.utils.load_config")
        mocked_load_config.side_effect = FileNotFoundError
        config = get_config()
        assert config == default_configs

class TestLoadConfig:
    def test_config_file_does_not_exist(self, delete_config_file):
        with pytest.raises(FileNotFoundError):
            load_config()

    def test_config_file_does_exist(self, create_valid_config_file):
        config = load_config()
        assert type(config) == str

@pytest.fixture
def apply_user_config_obj(request):
    marker = request.node.get_closest_marker("config_data")
    if marker is None:
        data = None
    else:
        data = marker.args[0]
    return data

class TestMergeUserConfigWithDefaults:
    @pytest.mark.config_data({})
    def test_when_not_overwritten(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == default_configs

    @pytest.mark.config_data({
        "RESUME_YAML_FILENAME": "custom.yml"
    })
    def test_when_overwritten_with_string(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == {
            "RESUME_YAML_FILENAME": ["custom.yml"]
        }

    @pytest.mark.config_data({
        "RESUME_YAML_FILENAME": ["custom.yml"]
    })
    def test_when_overwritten_with_list(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == {
            "RESUME_YAML_FILENAME": ["custom.yml"]
        }

    @pytest.mark.config_data({
        "custom_config": ["custom_value"]
    })
    def test_ignore_unsupported_config(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == default_configs

class TestValidateConfigTxt:
    def test_when_dict(self, mocker):
        mock = mocker.patch("resumaker.utils.yaml_to_pyobj")
        mock.return_value = {}
        config = validate_config_txt('')
        assert config == {}

    def test_when_list(self, mocker, capsys):
        mock = mocker.patch("resumaker.utils.yaml_to_pyobj")
        mock.return_value = []

        config = validate_config_txt('')

        captured = capsys.readouterr()
        assert captured.out == "config.yml is not valid! Using default configs.\n"
        assert config == {}

    def test_when_None(self, mocker, capsys):
        mock = mocker.patch("resumaker.utils.yaml_to_pyobj")
        mock.return_value = None

        config = validate_config_txt('')

        captured = capsys.readouterr()
        assert captured.out == "config.yml is not valid! Using default configs.\n"
        assert config == {}