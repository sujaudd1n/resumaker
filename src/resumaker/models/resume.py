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
        # name,
        # location,
        # contact,
        # summary,
        # education,
        # links,
        # skills,
        # work_experience,
        # projects,
    ):
        self.values = values
        self.template = template

        self.contact = Contact(name, location, contact)
        # self.summary = Summary(summary)
        # self.education = Education(education)
        # self.skills = Skills(skills)
        # self.work_experience = WorkExperience(work_experience)
        # self.projects = Project(projects)
        # self.links = Links(links)

        self.setup_sections = [
            self.template.get_license(),
            self.template.get_preamble(),
            self.template.get_contact(),
        ]

        # self.internal_sections = [self.summary, self.education, self.skills, self.links]
        self.internal_sections = order

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
    def generate_tex(self):
        self.template.get_tex("contact", self.values["contact"])


class Summary:
    def generate_tex(self):
        self.template.get_tex("summary", self.values["summary"])


class Education:
    def generate_tex(self):
        self.template.get_tex("education", self.values["education"])


class Links:
    def generate_tex(self):
        self.template.get_tex("links", self.values["education"])


class Skills:
    pass


class WorkExperience:
    pass

    def __init__(self, work_experience):
        self.work_experience = work_experience

    def generate_tex(self):
        we_complete_tex_template = Template(template["work_experience"]["complete"])
        we_single_tex_template = Template(template["work_experience"]["single"])
        contribution_tex_template = Template(
            template["work_experience"]["single-contribution"]
        )

        single_tex = []
        for experience in self.work_experience:
            company_name = experience["company-name"]
            company_location = experience["location"]
            position = experience["position"]
            duration = experience["duration"]

            contribution_tex = []
            for contribution in experience["contributions"]:
                contribution_tex.append(
                    contribution_tex_template.substitute(contribution=contribution)
                )

            single_tex.append(
                we_single_tex_template.substitute(
                    company_name=company_name,
                    company_location=company_location,
                    position=position,
                    duration=duration,
                    all_contributions="\n".join(contribution_tex),
                )
            )

        we_tex = we_complete_tex_template.substitute(
            all_work_experiences="\n".join(single_tex)
        )

        return we_tex


class Project:
    pass

    def generate_tex(self):
        project_complete_tex_template = Template(template["projects"]["complete"])
        project_single_tex_template = Template(template["projects"]["single"])
        detail_tex_template = Template(template["projects"]["single-detail"])

        single_tex = []
        for project in self.projects:
            project_name = project["name"]
            technologies = ", ".join(project["techstack"])

            detail_tex = []
            for detail in project["details"]:
                detail_tex.append(detail_tex_template.substitute(detail=detail))

            single_tex.append(
                project_single_tex_template.substitute(
                    project_name=project_name,
                    technologies=technologies,
                    all_details="\n".join(detail_tex),
                )
            )

        project_tex = project_complete_tex_template.substitute(
            all_projects="\n".join(single_tex)
        )

        return project_tex
