from mongoengine import Document, StringField, BooleanField

class User(Document):
    username = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    role = StringField(required=True, choices=['admin', 'user'])
    is_active = BooleanField(default=True)

    meta = {'collection': 'users'}

class Project(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    created_by = StringField(required=True)

    meta = {'collection': 'projects'}
