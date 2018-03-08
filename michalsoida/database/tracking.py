from datetime import datetime

from pytz import utc, timezone
from flask import g, request
from peewee import CharField, TextField, IntegerField, FloatField
from playhouse.fields import PickleField
from playhouse.postgres_ext import DateTimeTZField, ArrayField

from .peewee import BaseModel

tz = timezone('Europe/Warsaw')


class PrintStorage(object):
    """Fake storage container for debugging."""

    url = None
    scheme = None
    host = None
    path = None
    method = None
    referrer = None
    remote_addr = None
    real_ip = None
    forwarded_proto = None
    connecting_ip = None
    ip_country = None
    visitor = None
    status = None
    args = None
    user_agent = None
    access_route = None
    headers = None
    cookies = None
    date = None
    speed = None

    def print(self):
        """Print data that would be stored."""
        print("url: {}".format(self.url))
        print("scheme: {}".format(self.scheme))
        print("host: {}".format(self.host))
        print("path: {}".format(self.path))
        print("method: {}".format(self.method))
        print("referrer: {}".format(self.referrer))
        print("remote address: {}".format(self.remote_addr))
        print("real ip: {}".format(self.real_ip))
        print("forwarded proto: {}".format(self.forwarded_proto))
        print("connecting ip: {}".format(self.connecting_ip))
        print("ip country: {}".format(self.ip_country))
        print("visitor: {}".format(self.visitor))
        print("status: {}".format(self.status))
        print("args: {}".format(self.args))
        print("user agent: {}".format(self.user_agent['browser']))
        print("access route: {}".format(self.access_route))
        print("headers: {}".format(self.headers))
        print("cookies: {}".format(self.cookies))
        print("date: {}".format(
            self.date.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')))
        print("speed: {}".format(self.speed))

    def save(self):
        self.print()


class PostgresStorage(BaseModel, PrintStorage):
    """Storage container for Postgresql database."""

    date = DateTimeTZField()
    url = TextField(null=True)
    scheme = TextField(null=True)
    host = TextField(null=True)
    path = TextField(null=True)
    method = CharField(null=True)
    referrer = TextField(null=True)
    remote_addr = TextField(null=True)
    real_ip = CharField(null=True)
    forwarded_proto = CharField(null=True)
    connecting_ip = CharField(null=True)
    ip_country = CharField(null=True)
    visitor = TextField(null=True)
    status = IntegerField(null=True)
    args = PickleField(null=True)
    user_agent = PickleField(null=True)
    access_route = ArrayField(CharField, null=True)
    headers = PickleField(null=True)
    cookies = PickleField(null=True)
    speed = FloatField(null=True)

    class Meta:
        table_name = 'tracking'


class Tracking(object):
    """Flask application usage tracker."""

    def __init__(self, app, db=True):
        if db:
            self.storage = PostgresStorage
        else:
            self.storage = PrintStorage
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def should_track(self):
        """Check if page should be tracked."""
        if request.path.startswith('/static'):
            return False
        return True

    def before_request(self):
        if not self.should_track():
            return
        g.start_time = datetime.now(utc)

    def after_request(self, response):
        if not self.should_track():
            return response
        data = self.storage()
        data.url = request.url
        data.scheme = request.scheme
        data.host = request.host
        data.path = request.path
        data.method = request.method
        data.referrer = request.referrer
        data.remote_addr = request.remote_addr
        data.status = response.status_code
        data.args = dict(request.args)

        data.user_agent = dict(
            string=request.user_agent.string,
            platform=request.user_agent.platform,
            browser=request.user_agent.browser,
            version=request.user_agent.version,
            language=request.user_agent.language)

        data.access_route = list(request.access_route)
        data.headers = dict(request.headers)

        # Put popular headers in their own fields
        data.real_ip = data.headers.pop('X-Real-Ip', None)
        data.forwarded_proto = data.headers.pop('X-Forwarded-Proto', None)
        data.connecting_ip = data.headers.pop('Cf-Connecting-Ip', None)
        data.ip_country = data.headers.pop('Cf-Ipcountry', None)
        data.visitor = data.headers.pop('Cf-Visitor', None)

        # Remove headers that are stored in other fields
        data.headers.pop('Cookie', None)
        data.headers.pop('User-Agent', None)
        data.headers.pop('Host', None)
        data.headers.pop('X-Forwarded-For', None)

        # Remove connection-related headers
        data.headers.pop('Connection', None)
        data.headers.pop('Content-Length', None)
        data.headers.pop('Content-Type', None)
        data.headers.pop('Cache-Control', None)
        data.headers.pop('Accept', None)
        data.headers.pop('Accept-Encoding', None)
        data.headers.pop('Accept-Language', None)
        data.headers.pop('Upgrade-Insecure-Requests', None)
        data.headers.pop('Cf-Ray', None)

        data.cookies = dict(request.cookies)
        # Remove all CloudFlare cookies
        for i in list(data.cookies.keys()):
            if i.startswith('__') or i.startswith('cf'):
                data.cookies.pop(i)
        data.date = datetime.now(utc)
        start_time = g.pop('start_time', None)
        if start_time is not None:
            data.speed = (datetime.now(utc) - start_time).total_seconds()
        data.save()
        return response


tables_to_create = [
    PostgresStorage,
]
