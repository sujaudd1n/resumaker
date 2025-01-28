import json
import os
from string import Template
from resumaker.config import BASE_DIR
from resumaker.utils import render_yaml_txt


class ResumeTemplate:
    "An interface between resume and actual template string."

    def __init__(self, name):
        self.name = name
        self.tex_template_obj = self.get_template_obj()
        # self.contact = ContactTemplate()

    def get_template_obj(self):
        with open(
            os.path.join(BASE_DIR, "templates", self.name, "tex_template.yml")
        ) as f:
            tex = f.read()

            tex_obj = render_yaml_txt(tex)
            return tex_obj

    def get_tex(section, values):
        return getattr(self, section).render_tex(
            values, self.tex_template_obj["contact"]
        )

    def render_tex(self):
        pass


class ContactTemplate:
    def __init__(self, values, template):
        self.values = values
        self.template = template

    def render_tex(self):
        pyTemplate = Template(self.template)
        result = pyTemplate.substitute(
            name=self.values["name"],
            location=self.values["location"],
            phone=self.values["phone"],
            email=self.values["email"],
            linkedin=self.values["linkedin"],
            github=self.values["github"],
        )
        return result


class SummaryTemplate:
    def __init__(self, values, template):
        self.values = values
        self.template = template

    def render_tex(self):
        pyTemplate = Template(self.template)
        result = pyTemplate.substitute(
            title=self.values["title"],
            text=self.values["text"],
        )
        return result


class EducationTemplate:
    def __init__(self, values, template):
        self.values = values
        self.template = template

    def render_tex(self):
        py_complete_template = Template(self.template["complete"])
        py_single_template = Template(self.template["single"])
        py_acheivement_template = Template(self.template["acheivement"])

        rendered_single_educations = []
        for institute in self.values:
            rendered_acheivements = []
            for acheivement in institute["acheivements"]:
                rendered_acheivement = py_acheivement_template.substitute(acheivement=acheivement)
                rendered_acheivements.append(rendered_acheivement)
            rendered_single_education = py_single_template.substitute(
                name=institute["name"],
                duration=institute["duration"],
                degree=institute["degree"],
                location=institute["location"],
                all_acheivements=" ".join(rendered_acheivements),
            )
            rendered_single_educations.append(rendered_single_education)

        all_educations = "\n".join(rendered_single_educations)
        rendered_complete_education = py_complete_template.substitute(
            all_educations=all_educations
        )
        return rendered_complete_education
