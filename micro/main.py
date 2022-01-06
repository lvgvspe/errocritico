from flask import Flask, render_template

app = Flask(__name__)

@app.route ('/')
def ola():
    return "Olá, mundo! Teste 2"

@app.route ('/login')
def adeus():
    return render_template('index.html')