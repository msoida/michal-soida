from peewee import TextField

from .peewee import BaseModel


class Project(BaseModel):
    title = TextField()
    description = TextField()

    class Meta:
        order_by = ['title']


tables_to_create = [
    Project,
]
