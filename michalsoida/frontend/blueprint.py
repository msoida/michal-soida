from flask import (Blueprint, render_template, make_response,
                   url_for, request, abort, flash, redirect)
from flask_login import (current_user, login_required, login_url)
from webargs import fields, missing, validate
from webargs.flaskparser import use_kwargs

from ..database import Project


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


@frontend.route('/projekty/')
def projekty():
    projects = Project.select().order_by(Project.title_pl)
    return render_template('frontend/projekty.html', projects=projects,
                           user=current_user)


@frontend.route('/o-stronie/')
def o_stronie():
    return render_template('frontend/o-stronie.html')


@frontend.route('/en/')
def en_index():
    return render_template('frontend/about-me.html', english=True)


@frontend.route('/en/contact/')
def en_contact():
    return render_template('frontend/kontakt.html', english=True)


@frontend.route('/en/projects/')
def en_projects():
    projects = Project.select().order_by(Project.title_en)
    return render_template('frontend/projekty.html', english=True,
                           projects=projects, user=current_user)


@frontend.route('/en/about-page/')
def en_about_page():
    return render_template('frontend/about-page.html', english=True)


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


projekty_edit_args = {
    'project_id': fields.Int(required=True),
}


@frontend.route('/projekty/edit/')
@login_required
@use_kwargs(projekty_edit_args)
def projekty_edit(project_id):
    project = Project.get_by_id(project_id)
    return render_template('frontend/projekty-edit.html', project=project)


save_project_args = {
    'project_id': fields.Int(required=True),
}


@frontend.route('/edit/submit', methods=['POST'])
@login_required
@use_kwargs(save_project_args)
def save_project(project_id):
    return redirect(url_for('.projekty'))
