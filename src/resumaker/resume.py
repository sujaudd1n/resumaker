import subprocess
import os
import shutil
from pathlib import Path
from string import Template
from resumaker.template_str import template


class Resume:
    def __init__(
        self,
        name,
        location,
        contact,
        summary,
        education,
        links,
        skills,
        work_experience,
        projects,
        order,
    ):
        self.contact = Contact(name, location, contact)
        self.summary = Summary(summary)
        self.education = Education(education)
        self.skills = Skills(skills)
        self.work_experience = WorkExperience(work_experience)
        self.projects = Project(projects)
        self.links = Links(links)

        self.setup_sections = [
            template["license"],
            template["setup"],
            self.contact.generate_tex(),
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
        filepath = Path(__file__).parent.parent.parent.joinpath(
            f"templates/{filename}.tex"
        )
        with open(filepath, "w") as f:
            text = self.generate_tex()
            f.write(text)

    def build(self, filename):
        self.write_tex(filename)
        filepath = Path(__file__).parent.parent.parent.joinpath(
            f"templates/{filename}.tex"
        )
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


class Education:
    def __init__(self, education):
        self.education = education

    def generate_tex(self):
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

    def __str__(self):
        return f"{self.education[0].name}"


class Links:
    def __init__(self, links):
        self.links = links

    def generate_tex(self):
        links_complete_tex_template = Template(template["links"]["complete"])
        single_tex = []
        for link_name, link_content in self.links.items():
            links_single_tex_template = Template(template["links"]["single"])
            single_tex.append(
                links_single_tex_template.substitute(
                    link_title=link_content["name"],
                    link_url=link_content["url"],
                    link_url_text=link_content["url_text"],
                )
            )
        links_tex = links_complete_tex_template.substitute(
            all_links="\n".join(single_tex)
        )
        return links_tex

    def __str__(self):
        return f"{self.title}"


class Skills:
    def __init__(self, skills):
        self.skills = skills

    def generate_tex(self):
        skills_complete_tex_template = Template(template["skills"]["complete"])
        single_tex = []
        for skill_topic, skills_list in self.skills.items():
            skill_single_tex_template = Template(template["skills"]["single"])
            single_tex.append(
                skill_single_tex_template.substitute(
                    skill_topic=skill_topic[0].upper() + skill_topic[1:],
                    skills_list=", ".join(skills_list),
                )
            )
        skills_tex = skills_complete_tex_template.substitute(
            all_skills="\n".join(single_tex)
        )
        return skills_tex

    def __str__(self):
        return f"{self.title}"


class WorkExperience:
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
    def __init__(self, projects):
        self.projects = projects

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
