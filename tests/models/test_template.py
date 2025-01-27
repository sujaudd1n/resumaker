import pytest
from resumaker.models.template import ContactTemplate
from .tex_template import tex_template


class TestContactTemplate:
    @pytest.fixture
    def contactTemplate(self):
        contactTemplate = ContactTemplate(tex_template["contact"])
        return contactTemplate

    def test_get_tex(self, contactTemplate):
        tex = contactTemplate.get_tex()
        assert tex == tex_template["contact"]

    def test_render_tex(self, contactTemplate):
        values = {
            "name": "test",
            "location": "location",
            "phone": "phone",
            "email": "email",
            "linkedin": "linkedin",
            "github": "github",
        }
        tex = contactTemplate.render_tex(values)
        assert (
            tex
            == r"""
\name{test}
\address{location}
\address{\raisebox{-2px}{\includegraphics[width=10px]{icons/phone.png}}  phone \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/mail.png}} email  \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/linkedin.png}} \href{https://www.linkedin.com/in/linkedin/}{linkedin.com/in/linkedin} \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/github.png}} \href{https://github.com/github}{github.com/github}}
"""
        )
