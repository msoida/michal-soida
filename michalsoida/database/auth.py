from flask_login import UserMixin
from passlib.context import CryptContext
from passlib.pwd import genword
from peewee import CharField, TextField, DoesNotExist

from .peewee import BaseModel

pwd_context = CryptContext(schemes=['sha512_crypt'])


class User(BaseModel, UserMixin):

    username = CharField(unique=True)
    _password = TextField()
    session_token = CharField(unique=True)
    apikey = CharField(unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = pwd_context.encrypt(password)
        self.session_token = genword(length=50)

    @password.deleter
    def password(self):
        del self._password
        del self.session_token

    def verify_password(self, password):
        if self.password is None:
            return False
        valid, new_hash = pwd_context.verify_and_update(password,
                                                        self.password)
        if valid:
            if new_hash:
                self._password = new_hash
                self.session_token = genword(length=50)
                self.save()
            return True
        return False

    def get_id(self):
        return self.session_token


tables_to_create = [
    User,
]
