from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from errocritico.auth import login_required
from errocritico.db import get_db
from datetime import date
from geopy.geocoders import Nominatim
import urllib.request,  json
import psycopg2.extras

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur=db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username, avatar'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cur.fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                'INSERT INTO posts (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = cur.fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Título é necessário.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                'UPDATE posts SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/profile/<string:username>')
@login_required
def profile(username):
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        'SELECT id, username, password, email, name, surname, location, country, state, zipcode, aboutme, birth, gender, avatar, private_profile, private_email, private_zipcode, private_birth, private_gender'
        ' FROM users WHERE username = %s', (username,)
    )
    user = cur.fetchall()
    cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cur2.fetchall()
    for u in user:
        age = date.today().year - int(u['birth'].split('-')[0]) - ((date.today().month, date.today().day) < (int(u['birth'].split('-')[1]), int(u['birth'].split('-')[2])))
    return render_template('blog/profile.html', user=user, posts=posts, age=age)

@bp.route('/map')
@login_required
def map():
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        'SELECT id, username, password, email, name, surname, location, country, state, zipcode, aboutme, birth, gender, private_profile, private_email, private_zipcode, private_birth, private_gender'
        ' FROM users'
    )
    users = cur.fetchall()

    local = []
    IDs = []

    for u in users:
        if len(u['zipcode']) == 8:
            with urllib.request.urlopen(f"https://viacep.com.br/ws/{u['zipcode']}/json") as url:
                address = json.loads(url.read().decode())
                if address.get('erro'):
                    pass
                else:
                    geolocator = Nominatim(user_agent="test_app")
                    location = geolocator.geocode(address['logradouro'].split('-')[0] + ", " + address['bairro'] + ", " + address['localidade'])
                    local.append({'local': location, 'username': u['username']})
                    IDs.append(u['id'])

    aurelio = dict(zip(IDs, local))

    return render_template('blog/map.html', aurelio=aurelio, location=location)
