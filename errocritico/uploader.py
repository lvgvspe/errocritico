import os
from flask import (
Blueprint, flash, g, request, redirect, url_for, render_template,
)
from werkzeug.exceptions import RequestEntityTooLarge
import cloudinary
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
                upload_result = cloudinary.uploader.upload(file, public_id = "g.user['username']")
                #file.save(os.path.join(os.path.abspath(os.curdir), 'errocritico/static/avatars', str(g.user['id'])))
                return upload_result
    except RequestEntityTooLarge:
        flash('Arquivo deve ter 5mb ou menos')
    return render_template('blog/upload.html')
