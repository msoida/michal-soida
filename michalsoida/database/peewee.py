from datetime import datetime

from pytz import utc
from peewee import Model, PrimaryKeyField, JOIN
from playhouse.postgres_ext import PostgresqlExtDatabase

from ..settings import postgres_db, postgres_user


db = PostgresqlExtDatabase(postgres_db, user=postgres_user,
                           register_hstore=False)


class BaseModel(Model):
    """A base model for Postgresql database."""
    class Meta:
        database = db


class BigPrimaryKeyField(PrimaryKeyField):
    db_field = 'bigserial'


def nowutc():
    return datetime.now(utc)
