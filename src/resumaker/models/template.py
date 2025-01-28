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
        education_tex_template = Template(template["education"]["complete"])
        single_education_tex_template = Template(template["education"]["single"])
        acheivement_tex_template = Template(template["education"]["acheivement"])

        single_education_tex_list = []
        for institute in self.education:
            acheivement_tex = []
            for acheivement in institute["acheivements"]:
                ra = acheivement_tex_template.substitute(single_acheivement=acheivement)
                acheivement_tex.append(ra)
            single_education_tex = single_education_tex_template.substitute(
                institution_name=institute["name"],
                duration=institute["duration"],
                degree=institute["degree"],
                institution_location=institute["location"],
                all_acheivements="".join(acheivement_tex),
            )
            single_education_tex_list.append(single_education_tex)

        all_education = "\n".join(single_education_tex_list)
        all_education_tex = education_tex_template.substitute(
            all_education=all_education
        )
        return all_education_tex
