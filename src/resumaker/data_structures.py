import subprocess
import os
import shutil
from pathlib import Path
from string import Template
from .template import template


class Resume:
    def __init__(self, name, location, contact, summary):
        self.contact = Contact(name, location, contact)
        self.summary = Summary(summary)
        # self.skills = Skills()
        # self.work_experience = WorkExperience()
        # self.projects = Project()
        # self.education = Education()
        # self.links = Links()

    def generate_tex(self):
        chunks = []

        chunks.append(template["license"])
        chunks.append(template["setup"])

        contact_tex = self.contact.generate_tex()
        chunks.append(contact_tex)

        internal_chunks = []
        summary_tex = self.summary.generate_tex()
        internal_chunks.append(summary_tex)

        main_content_str = "\n".join(internal_chunks)
        main_tex_template = Template(template["main"])
        main_tex = main_tex_template.substitute(CONTENT=main_content_str)
        chunks.append(main_tex)

        return "\n".join(chunks)

    def write_tex(self):
        filepath = Path(__file__).parent.parent.parent.joinpath("templates/resume.tex")
        print(filepath)
        with open(filepath, "w") as f:
            text = self.generate_tex()
            f.write(text)

    def build(self):
        self.write_tex()
        filepath = Path(__file__).parent.parent.parent.joinpath("templates/resume.tex")
        old_cwd = os.getcwd()
        newdir = os.path.dirname(filepath)
        os.chdir(newdir)
        cmpr = subprocess.run(["pdflatex", filepath])
        print(cmpr.returncode)
        if cmpr.returncode != 0:
            raise Exception
        shutil.copy("resume.pdf", os.path.join(old_cwd, "resume.pdf"))
        for ext in ["pdf", "log", "out", "tex", "aux"]:
            os.remove("resume." + ext)

    def __str__(self):
        return f"{self.name}"


class Contact:
    def __init__(self, name, location, contact):
        self.name = name
        self.location = location
        self.phone = contact["phone"]
        self.email = contact["email"]
        self.linkedin = contact["linkedin"]
        self.github = contact["github"]

    def generate_tex(self):
        template_str = Template(template["contact"])
        result = template_str.substitute(
            name=self.name,
            location=self.location,
            phone=self.phone,
            email=self.email,
            linkedin=self.linkedin,
            github=self.github,
        )
        return result

    def __str__(self):
        return f"{self.phone}"


class Summary:
    def __init__(self, summary):
        self.title = summary["title"]
        self.text = summary["text"]

    def generate_tex(self):
        summary_tex_template = Template(template["summary"])
        summary_tex = summary_tex_template.substitute(
            title=self.title,
            text=self.text,
        )
        return summary_tex


    def __str__(self):
        return f"{self.title}"
