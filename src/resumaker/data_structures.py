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
        chunks.append(template["setup"])
        template_str = Template(template["main"])

        contact_tex = self.contact.generate_tex()
        chunks.append(contact_tex)
        result = template_str.safe_substitute(CONTENT='hello')
        chunks.append(result)

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
        subprocess.run(["pdflatex", filepath])
        shutil.copy("resume.pdf", os.path.join(old_cwd,"resume.pdf"))
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
        template_str = template["contact"]
        return template_str


    def __str__(self):
        return f"{self.phone}"


class Summary:
    def __init__(self, summary):
        self.title = summary["title"]
        self.text = summary["text"]

    def __str__(self):
        return f"{self.title}"
