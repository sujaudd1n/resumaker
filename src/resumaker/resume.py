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

    def generate_tex(self):
        chunks = []

        chunks.append(template["license"])
        chunks.append(template["setup"])
        contact_tex = self.contact.generate_tex()
        chunks.append(contact_tex)

        internal_chunks = []
        summary_tex = self.summary.generate_tex()
        internal_chunks.append(summary_tex)
        skills_tex = self.skills.generate_tex()
        internal_chunks.append(skills_tex)
        links_tex = self.links.generate_tex()
        internal_chunks.append(links_tex)

        main_content_str = "\n".join(internal_chunks)
        main_tex_template = Template(template["main"])
        main_tex = main_tex_template.substitute(CONTENT=main_content_str)
        chunks.append(main_tex)

        return "\n".join(chunks)

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
