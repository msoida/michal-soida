from locale import setlocale, LC_ALL, Error as LocaleError

from pytz import utc, timezone
from flask import Flask, render_template

from .settings import secret_key
# from .database import db, Tracking
from .database import db
from .auth import auth, login_manager
from .frontend import frontend


# ----------------   VARIABLES   --------------- #


try:
    setlocale(LC_ALL, ('pl_PL', 'UTF-8'))
except LocaleError:
    print('WARNING: pl_PL locale not installed, using default')

tz = timezone('Europe/Warsaw')

app = Flask(__name__)
app.secret_key = secret_key
app.jinja_env.globals.update(utc=utc, tz=tz)

login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(frontend)


@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# tracking = Tracking(app)


# -----------------   ERRORS   ----------------- #


error500_name = 'Internal Server Error'
error500_description = ('The server has encountered an internal error'
                        ' and was unable to complete your request.'
                        ' Either the server is overloaded or there is'
                        ' an error in the application.')


@app.errorhandler(400)  # Bad Request
@app.errorhandler(401)  # Unauthorized
@app.errorhandler(403)  # Forbidden
@app.errorhandler(405)  # Method Not Allowed
@app.errorhandler(406)  # Not Acceptable
@app.errorhandler(408)  # Request Timeout
@app.errorhandler(409)  # Conflict
@app.errorhandler(410)  # Gone
@app.errorhandler(411)  # Length Required
@app.errorhandler(412)  # Precondition Failed
@app.errorhandler(413)  # Request Entity Too Large
@app.errorhandler(414)  # Request URI Too Long
@app.errorhandler(415)  # Unsupported Media Type
@app.errorhandler(416)  # Request Range Not Satisfiable
@app.errorhandler(417)  # Expectation Failed
@app.errorhandler(418)  # I'm a teapot
@app.errorhandler(428)  # Precondition Required
@app.errorhandler(429)  # Too Many Requests
@app.errorhandler(431)  # Request Header Fields Too Large
@app.errorhandler(500)  # Internal Server Error
@app.errorhandler(501)  # Not Implemented
@app.errorhandler(502)  # Bad Gateway
@app.errorhandler(503)  # Service Unavailable
def error_page(error):
    try:
        error_name = error.name
        error_code = error.code
        error_description = error.description
    except Exception:
        # Not a standard HTTP error, replacing with 500
        error_name = error500_name
        error_code = 500
        error_description = error500_description
    response = (render_template('error.html', error_name=error_name,
                                error_code=error_code,
                                error_description=error_description),
                error_code)
    return response


@app.errorhandler(404)  # Not Found
def error_page_404(error):
    return render_template('error-404.html'), 404


@app.errorhandler(422)  # Unprocessable Entity
def error_422(error):
    error_name = error.name
    error_code = error.code
    error_description = error.description
    # Webargs attaches additional metadata to the `data` attribute
    exc = getattr(error, 'exc')
    if exc:
        # Get validations from the ValidationError object
        messages = exc.messages
    else:
        messages = ['Invalid request']
    response = (render_template('error.html', error_name=error_name,
                                error_code=error_code,
                                error_description=error_description,
                                messages=messages),
                error_code)
    return response
