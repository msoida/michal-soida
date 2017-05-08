from datetime import datetime

from flask import (Blueprint, render_template, make_response,
                   url_for, request, abort, flash, redirect)
from flask_login import (current_user, login_required, login_url)
from pytz import timezone

from .database import Project


tz = timezone('Europe/Warsaw')

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/favicon.ico')
def favicon_ico():
    return redirect(url_for('static', filename='favicon.ico'))


@frontend.route('/robots.txt')
def robots_txt():
    return 'User-agent: *\nDisallow: \n'


@frontend.route('/')
def index():
    return render_template('frontend/o-mnie.html')


@frontend.route('/kontakt/')
def kontakt():
    return render_template('frontend/kontakt.html')


@frontend.route('/pgp/')
def pgp():
    return render_template('frontend/pgp.html')


@frontend.route('/projekty/')
def projekty():
    projects = list(Project.select())
    return render_template('frontend/projekty.html', projects=projects)


@frontend.route('/o-stronie/')
def o_stronie():
    t = datetime.now(tz).strftime('%d.%m.%Y %H:%M:%S')
    return render_template('o-stronie.html', data_godzina=t)


@frontend.route('/apple-touch-icon-precomposed.png')
@frontend.route('/apple-touch-icon-144x144-precomposed.png')
def apple_touch_icon():
    return redirect(url_for('static',
                            filename='apple-touch-icon-precomposed.png'))


@frontend.route('/keybase.txt')
@frontend.route('/.well-known/keybase.txt')
def keybase_txt():
    return redirect(url_for('static', filename='keybase.txt'))


@frontend.route('/o-mnie/')
@frontend.route('/index.html')
@frontend.route('/index.php')
def red_index():
    return redirect(url_for('index'))


@frontend.route('/pogoda/')
@frontend.route('/download/')
@frontend.route('/html2text/')
@frontend.route('/ipogoda/')
@frontend.route('/ipogoda/image.php')
@frontend.route('/ipogoda/index.html')
@frontend.route('/ipogoda/komentarz.php')
@frontend.route('/ipogoda/makeimage.php')
@frontend.route('/fuzzer/')
@frontend.route('/fuzzer/status')
@frontend.route('/covers/')
@frontend.route('/covers/form/')
@frontend.route('/covers/i/')
@frontend.route('/iwebkit/')
@frontend.route('/rsscovers/')
@frontend.route('/rmf/')
@frontend.route('/skaner/')
def file_deleted():
    abort(410)
