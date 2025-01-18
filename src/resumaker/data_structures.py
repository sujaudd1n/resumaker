class Resume:
    def __init__(self, name):
        self.contact = Contact()
        self.summary = Summary()
        self.skills = Skills()
        self.work_experience = WorkExperience()
        self.projects = Project()
        self.education = Education()
        self.links = Links()


class Contact:
    def __init__(self, contact):
        self.phone =  contact['phone']
        self.email =  contact['email']
        self.linkedin =  contact['linkedin']
        self.github = contact['github']
    
    def __str__(self):
        return f"{self.phone}"


class Summary:
    def __init__(self, summary):
        self.title =  summary['title']
        self.text =  summary['text']
    
    def __str__(self):
        return f"{self.title}"