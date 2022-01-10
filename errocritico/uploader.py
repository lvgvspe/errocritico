import os
from flask import (
Blueprint, Flask, flash, g, request, redirect, url_for, render_template, send_from_directory, abort
)
from werkzeug.utils import secure_filename

bp = Blueprint('uploader', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/upload', methods=['GET', 'POST'])
def upload_avatar():
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
            file.save(os.path.join('/home/lvgvspe/errocritico/errocritico/static/avatars', g.user['username']))
            return redirect(url_for('blog.profile', username=g.user['username']))
    return render_template('blog/upload.html')