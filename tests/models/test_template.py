import pytest
from resumaker.models.template import *
from .tex_template import tex_template


class TestResumeTemplate:
    def test_template_import(self):
        resumeTemplate = ResumeTemplate("t1")
        template_dict = resumeTemplate.get_template_obj()
        assert type(template_dict) == dict


class TestContactTemplate:
    @pytest.fixture
    def contactObj(self):
        values = {
            "name": "test",
            "location": "location",
            "phone": "phone",
            "email": "email",
            "linkedin": "linkedin",
            "github": "github",
        }
        template = "$name$location$phone$email$linkedin$github"

        contactTemplate = ContactTemplate(values, template)
        return contactTemplate

    def test_render_tex(self, contactObj):
        tex = contactObj.render_tex()
        assert tex == "testlocationphoneemaillinkedingithub"


class TestSummaryTemplate:
    @pytest.fixture
    def summaryObj(self):
        values = {
            "title": "summary title",
            "text": "summary text",
        }
        template = "$title $text"

        summaryTemplate = SummaryTemplate(values, template)
        return summaryTemplate

    def test_render_tex(self, summaryObj):
        tex = summaryObj.render_tex()
        assert tex == "summary title summary text"
