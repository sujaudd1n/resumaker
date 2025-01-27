from string import Template

class ResumeTemplate:
    "An interface between resume and actual template string."

    def __init__(
        self,
        license,
        setup,
        main,
        contact,
        education,
        summary,
        skills,
        work_experience,
        prjects,
    ):
        "Each parameter is a latex string"
        self.license = license

    def get_tex(self):
        pass

    def render_tex(self):
        pass


class ContactTemplate:
    def __init__(self, contact_tex):
        self.contact_tex = contact_tex

    def get_tex(self):
        return self.contact_tex

    def render_tex(self, values):
        return Template(self.contact_tex.substitute(values))
