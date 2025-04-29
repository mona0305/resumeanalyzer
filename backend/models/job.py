
from mongoengine import Document, StringField, ListField

class Job(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    required_skills = ListField(StringField())
    location = StringField()
    recruiter_id = StringField()  # Link to the recruiter (User)
    