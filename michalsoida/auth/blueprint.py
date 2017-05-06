from flask import (Blueprint, render_template, make_response,
                   url_for, request, abort, flash, redirect)
from flask_login import (LoginManager, AnonymousUserMixin,
                         login_user, logout_user, login_required,
                         current_user)
from passlib.pwd import genword

from ..database import User, DoesNotExist

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
    try:
        return User.get(User.session_token == session_token)
    except DoesNotExist:
        return None


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if request.method == 'POST':
        api_key = request.form.get('api_key')
    if api_key:
        try:
            return User.get(User.apikey == api_key)
        except DoesNotExist:
            return None
    return None


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    if next is None:
        next = url_for('frontend.index')
    username = ''
    password = ''
    remember = False
    if request.method == 'POST':
        next = request.form['next']
        username = request.form['username']
        password = request.form['password']
        if request.form.get('remember') == 'yes':
            remember = True
        try:
            user = User.get(User.username == username)
        except DoesNotExist:
            user = None
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


@auth.route('/api/create/')
@login_required
def api_create():
    user = current_user
    user.apikey = genword(length=25)
    user.save()
    flash('API key created')
    return redirect(url_for('index'))
