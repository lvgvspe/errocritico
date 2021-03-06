import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from errocritico.db import get_db
import errocritico as app
import psycopg2.extras
import cloudinary.api

cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        location = request.form['location']
        birth = request.form['birth']
        db = get_db()
        error = None

        if not username:
            error = 'Usuário é necessário.'
        elif not password:
            error = 'Senha é necessária.'
        elif not email:
            error = 'E-mail é necessário.'
        elif not name:
            error = 'Nome é necessário.'
        elif not birth:
            error = 'Idade é necessária.'

        if error is None:
            try:
                cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute(
                    "INSERT INTO users (username, password, email, name, surname, location, birth) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (username, generate_password_hash(password), email, name, surname, location, birth,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = cur.fetchone()

        if user is None:
            error = 'Usuário incorreto.'
        elif not check_password_hash(user['password'], password):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cur.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/<int:id>/userdelete', methods=('POST',))
@login_required
def delete(id, check_user=True):

    if check_user and id != g.user['id']:
        abort(403)

    else:
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM posts WHERE author_id = %s', (id,))
        cur.execute('DELETE FROM users WHERE id = %s', (id,))
        db.commit()
        cloudinary.api.delete_resources_by_tag(g.user['username'])
        cloudinary.api.delete_folder(g.user['username'])


    return redirect(url_for('auth.login'))

def get_user(id, check_user=True):
    cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        'SELECT id, username, password, email, name, surname, location, country, state, zipcode, aboutme, birth, gender, private_profile, private_email, private_zipcode, private_birth, private_gender'
        ' FROM users WHERE id = %s', (id,)
    )
    user = cur.fetchone()

    if user is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_user and id != g.user['id']:
        abort(403)

    return user

@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    user = get_user(g.user['id'])

    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'update_profile':
            username = request.form['username']
            email = request.form['email']
            name = request.form['name']
            surname = request.form['surname']
            location = request.form['location']
            country = request.form['country']
            state = request.form['state']
            zipcode = request.form['zipcode']
            aboutme = request.form['aboutme']
            birth = request.form['birth']
            gender = request.form['gender']
            private_profile = request.form.get('private_profile')
            private_email = request.form.get('private_email')
            private_zipcode = request.form.get('private_zipcode')
            private_birth = request.form.get('private_birth')
            private_gender = request.form.get('private_gender')
            error = None

            if not username:
                error = 'Usuário é necessário.'

            if not email:
                error = 'E-mail é necessário.'

            if not name:
                error = 'Nome é necessário.'

            if error is not None:
                flash(error)
            else:
                db = get_db()
                cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute(
                    'UPDATE users SET username = %s, email = %s, name = %s, surname = %s, location = %s, country = %s, state = %s, zipcode = %s, aboutme = %s, gender = %s, birth = %s, private_profile = %s, private_email = %s, private_zipcode = %s, private_birth = %s, private_gender = %s'
                    ' WHERE id = %s',
                    (username, email, name, surname, location, country, state, zipcode, aboutme, gender, birth, private_profile, private_email, private_zipcode, private_birth, private_gender, g.user['id'])
                )
                db.commit()
                return redirect(url_for('blog.profile', username=username))

        if form_name == 'update_password':
            old_password = request.form['old_password']
            password = request.form['password']
            password_check = request.form['password_check']
            error = None

            if not check_password_hash(user['password'], old_password):
                error = 'Senha incorreta.'

            if password != password_check:
                error = 'Senhas não combinam.'

            if error is not None:
                flash(error)
            else:
                db = get_db()
                cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute(
                    'UPDATE users SET password = %s'
                    ' WHERE id = %s',
                    (generate_password_hash(password), g.user['id'])
                )
                db.commit()
                return redirect(url_for('blog.profile', username=g.user['username']))


    return render_template('blog/settings.html', user=user)
