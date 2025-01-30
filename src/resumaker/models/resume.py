import subprocess
import os
import shutil
from pathlib import Path
from string import Template
from resumaker.template_str import template
from resumaker.config import get_config
from resumaker.models.template import ContactTemplate

config = get_config()
BASE_DIR = config["BASE_DIR"]


class Resume:
    def __init__(
        self,
        values,
        template,
        /,
        order,
    ):
        self.values = values
        self.template = template

        self.contact = Contact()
        self.summary = Summary()
        self.education = Education()
        self.skills = Skills()
        self.work_experience = WorkExperience()
        self.projects = Project()
        self.links = Links()

        self.setup_sections = [
            self.template.get_license(),
            self.template.get_preamble(),
            self.contact.generate_tex(
                self.template,
                self.values["contact"]
                | {"name": self.values["name"]}
                | {"location": self.values["location"]},
            ),
        ]

        # self.internal_sections = [self.summary, self.education, self.skills, self.links]
        self.internal_sections = [] #order

    def generate_tex(self):
        all_sections_tex_list = []
        for section in self.setup_sections:
            all_sections_tex_list.append(section)

        internal_sections_tex_list = []
        for section in self.internal_sections:
            tex = getattr(self, section).generate_tex()
            internal_sections_tex_list.append(tex)

        internal_tex_template = Template(template["main"])
        internal_tex_str = "\n".join(internal_sections_tex_list)
        rendered_internal_tex = internal_tex_template.substitute(
            CONTENT=internal_tex_str
        )

        all_sections_tex_list.append(rendered_internal_tex)

        return "\n".join(all_sections_tex_list)

    def write_tex(self, filename):
        filepath = BASE_DIR.joinpath(f"templates/{filename}.tex")
        with open(filepath, "w") as f:
            text = self.generate_tex()
            f.write(text)

    def build(self, filename):
        self.write_tex(filename)
        filepath = BASE_DIR.joinpath(f"templates/{filename}.tex")
        old_cwd = os.getcwd()
        newdir = os.path.dirname(filepath)
        os.chdir(newdir)
        cmpr = subprocess.run(["pdflatex", "-interaction=batchmode", filepath])
        # if cmpr.returncode != 0:
        # raise Exception
        shutil.move(filename + ".pdf", os.path.join(old_cwd, filename + ".pdf"))
        for ext in ["log", "out", "tex", "aux"]:
            os.remove(filename + "." + ext)
        os.chdir(old_cwd)

    def __str__(self):
        return f"{self.name}"


class Contact:
    def generate_tex(self, template, values):
        return template.get_tex("contact", values)


class Summary:
    def generate_tex(self, template, values):
        return template.get_tex("summary", values)


class Education:
    def generate_tex(self, template, values):
        return template.get_tex("education", values)


class Links:
    def generate_tex(self, template, values):
        return template.get_tex("links", values)


class Skills:
    def generate_tex(self, template, values):
        return template.get_tex("links", values)


class WorkExperience:
    def generate_tex(self, template, values):
        return template.get_tex("links", values)


class Project:
    def generate_tex(self, template, values):
        return template.get_tex("links", values)
