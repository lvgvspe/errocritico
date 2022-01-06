from flask import Flask

app = Flask(__name__)

@app.route ('/')
def app(event):
    return "Olá, mundo!"

@app.route ('/login')
def app(event):
    return "Hello, world!"