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


class TestEducationTemplate:
    @pytest.fixture
    def summaryObj(self):
        values = [
            {
                "name": "CLGY",
                "location": "LOCX",
                "degree": "DEGZ",
                "duration": "DUR3",
                "acheivements": ["A1", "A2", "A3"],
            },
            {
                "name": "CLGY2",
                "location": "LOCX2",
                "degree": "DEGZ2",
                "duration": "DUR32",
                "acheivements": ["A12", "A22", "A32"],
            },
        ]
        template = {
            "complete": "S $all_educations E",
            "single": "$degree $duration $name $location $all_acheivements",
            "acheivement": "$acheivement",
        }

        educationTemplate = EducationTemplate(values, template)
        return educationTemplate

    def test_render_tex(self, summaryObj):
        tex = summaryObj.render_tex()
        assert tex == (
            "S DEGZ DUR3 CLGY LOCX A1 A2 A3\nDEGZ2 DUR32 CLGY2 LOCX2 A12 A22 A32 E"
        )


class TestLinksTemplate:
    @pytest.fixture
    def linksObj(self):
        values = {
            "algorithms": [
                {
                    "name": "l1",
                    "url": "http://example.com/l1",
                    "url_text": "l1text",
                },
                {
                    "name": "l3",
                    "url": "http://example.com/l3",
                    "url_text": "l3text",
                },
            ],
            "open-source": [
                {
                    "name": "l2",
                    "url": "http://example.com/l2",
                    "url_text": "l2text",
                }
            ],
        }
        template = {
            "complete": "$all_links",
            "single": "$link_title $single_links",
            "single-link": "$link_url $link_url_text",
        }

        linksTemplate = LinksTemplate(values, template)
        return linksTemplate

    def test_render_tex(self, linksObj):
        tex = linksObj.render_tex()
        assert tex == (
            "Algorithms http://example.com/l1 l1text http://example.com/l3 l3text\n"
            "Open Source http://example.com/l2 l2text"
        )
