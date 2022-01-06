from flask import Flask, render_template, request
from deta import Deta
import models

deta = Deta('b09y7hmi_AFEApMypWh31wYJdM9JbkvjMMrvm5RKk')
db = deta.Base('simple_db')

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
        models.create_post(name, post)
        

    return render_template('home.html')

@app.route ('/posts')
def posts():
    return render_template('posts.html')

# if __name__ == '__main__':
#     posts()