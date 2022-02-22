import os
from flask import (
Blueprint, flash, g, request, redirect, url_for, render_template,
)
from werkzeug.exceptions import RequestEntityTooLarge
from errocritico.db import get_db
import psycopg2.extras
import cloudinary.uploader

bp = Blueprint('uploader', __name__)

cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/upload', methods=['GET', 'POST'])
def upload_avatar():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                upload_result = cloudinary.uploader.upload(file, tags = g.user['username'], public_id = f"{g.user['username']}/{g.user['username']}")
                db = get_db()
                cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute(
                    'UPDATE users SET avatar = %s'
                    ' WHERE id = %s',
                    (upload_result['secure_url'], g.user['id'])
                )
                db.commit()
                return redirect(url_for('blog.profile', username=g.user['username']))
    except RequestEntityTooLarge:
        flash('Arquivo deve ter 5mb ou menos')
    return render_template('blog/upload.html')
