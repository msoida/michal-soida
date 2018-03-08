from peewee import TextField

from .peewee import BaseModel


class Project(BaseModel):
    title = TextField()
    description = TextField()


tables_to_create = [
    Project,
]
