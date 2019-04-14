from flask import (Blueprint, render_template, make_response,
                   url_for, request, abort, flash, redirect)
from flask_login import (LoginManager, AnonymousUserMixin,
                         login_user, logout_user, login_required,
                         current_user)
from webargs import fields, missing
from webargs.flaskparser import parser, use_kwargs

from ..database import User

auth = Blueprint('auth', __name__, template_folder='templates')

login_required_message = 'Please log in to access this page.'
login_bad_message = 'Wrong username or password'
logout_message = 'Logout complete'


class AnonymousUser(AnonymousUserMixin):
    username = 'Anonymous User'
    password = ''
    session_token = ''
    apikey = ''

    def verify_password(self, password):
        return False


login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'auth.login'
login_manager.login_message = login_required_message


@login_manager.user_loader
def load_user(session_token):
    return User.get_or_none(User.session_token == session_token)


@login_manager.request_loader
def load_user_from_request(request):
    api_key = parser.parse_arg('api_key', fields.Str(), request)
    if api_key is not missing:
        return User.get_or_none(User.apikey == api_key)
    return None


login_args = {
    'next': fields.Str(missing=None),
    'username': fields.Str(missing=''),
    'password': fields.Str(missing=''),
    'remember': fields.Boolean(missing=False),
}


@auth.route('/login/', methods=['GET', 'POST'])
@use_kwargs(login_args)
def login(next, username, password, remember):
    if next is None:
        next = url_for('frontend.index')
    if request.method == 'POST':
        user = User.get_or_none(User.username == username)
        if user is not None:
            if user.verify_password(password):
                login_user(user, remember=remember)
                return redirect(next)
        flash(login_bad_message)
    return render_template('auth/login.html', next=next,
                           username=username)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(logout_message)
    return redirect(url_for('frontend.index'))
