class Template:
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
    def __init__(self, contact):
        self.contact = contact

    def get_tex(self):
        pass

    def render_tex(self):
        pass
