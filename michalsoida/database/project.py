from peewee import TextField, BlobField

from .peewee import BaseModel


class Project(BaseModel):
    title_pl = TextField()
    title_en = TextField()

    description_pl = TextField()
    description_en = TextField()

    thumbnail = BlobField(null=True)
    thumbnail_mimetype = TextField(null=True)

    content_pl = TextField()
    content_en = TextField()

tables_to_create = [
    Project,
]
