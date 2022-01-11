import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from errocritico.db import get_db

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

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email, name, surname, location) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, name, surname, location)
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
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

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
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

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
        db.execute('DELETE FROM user WHERE id = ?', (id,))
        db.commit()


    return redirect(url_for('auth.login'))

def get_user(id, check_user=True):
    user = get_db().execute(
        'SELECT id, username, password, email, name, surname, location'
        ' FROM user WHERE id = ?', (id,)
    ).fetchone()

    if user is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_user and id != g.user['id']:
        abort(403)

    return user

@bp.route('/profile/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_profile(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        location = request.form['location']
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
            db.execute(
                'UPDATE user SET username = ?, email = ?, name = ?, surname = ?, location = ?'
                ' WHERE id = ?',
                (username, email, name, surname, location, id)
            )
            db.commit()
            return redirect(url_for('blog.profile', username=username))

    return render_template('auth/update.html', user=user)