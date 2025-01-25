import subprocess
import os
import shutil
from pathlib import Path
from string import Template
from .template import template


class Resume:
    def __init__(self, name, location, contact, summary, links, skills):
        self.contact = Contact(name, location, contact)
        self.summary = Summary(summary)
        self.skills = Skills(skills)
        # self.work_experience = WorkExperience()
        # self.projects = Project()
        # self.education = Education()
        self.links = Links(links)

        self.setup_sections = [
            template["license"],
            template["setup"],
            self.contact.generate_tex(),
        ]

        self.internal_sections = [self.summary, self.skills, self.links]

    def generate_tex(self):
        all_sections_tex_list = []
        for section in self.setup_sections:
            all_sections_tex_list.append(section)

        internal_sections_tex_list = []
        for section in self.internal_sections:
            tex = section.generate_tex()
            internal_sections_tex_list.append(tex)

        internal_tex_template = Template(template["main"])
        internal_tex_str = "\n".join(internal_sections_tex_list)
        rendered_internal_tex = internal_tex_template.substitute(CONTENT=internal_tex_str)

        all_sections_tex_list.append(rendered_internal_tex)

        return "\n".join(all_sections_tex_list)

    def write_tex(self, filename):
        filepath = Path(__file__).parent.parent.parent.joinpath(
            f"templates/{filename}.tex"
        )
        print(filepath)
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
        cmpr = subprocess.run(["pdflatex", filepath])
        print(cmpr.returncode)
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


class Links:
    def __init__(self, links):
        self.links = links

    def generate_tex(self):
        links_complete_tex_template = Template(template["links"]["complete"])
        single_tex = []
        for link_name, link_content in self.links.items():
            print(link_name, link_content)
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
        print(links_tex)
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
