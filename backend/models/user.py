
from mongoengine import Document, StringField, ListField

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    skills = ListField(StringField())
    location = StringField()
    resume_path = StringField()
    