from flask import Flask, render_template

app = Flask(__name__)

@app.route ('/')
def ola():
    return "Erro crítico: em construção."

@app.route ('/login')
def adeus():
    return render_template('login.html')