import os
import pytest
from resumaker.utils import *

class TestReadFileTxt:
    @pytest.fixture
    def create_file(self, request):
        marker = request.node.get_closest_marker("create_file")
        if marker is None:
            data = None
        else:
            filename = marker.args[0]
            txt = marker.args[1]
        f = open(filename, 'w')
        f.write(txt)
        f.close()
        yield
        os.remove(filename)

    @pytest.fixture
    def delete_file(self):
        if os.path.exists("file.txt"):
            os.remove("file.txt")

    def test_file_does_not_exist(self, delete_file):
        with pytest.raises(FileNotFoundError):
            read_file_txt("file.txt")

    @pytest.mark.create_file("file.txt", "")
    def test_file_exists_and_empty(self, create_file):
        txt = read_file_txt("file.txt")
        assert txt == ""

    @pytest.mark.create_file("file.txt", "hello-world")
    def test_file_exists_and_not_empty(self, create_file):
        txt = read_file_txt("file.txt")
        assert txt == "hello-world"


