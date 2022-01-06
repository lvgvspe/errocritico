from flask import Flask, render_template, request
from models import create_post, get_posts

app = Flask(__name__)

@app.route ('/')
def ola():
    return "Erro crítico: em construção."

@app.route ('/login')
def adeus():
    return render_template('login.html')

@app.route ('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

    posts = get_posts()

    return render_template('home.html')