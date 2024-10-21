from flask import Flask
from flask import render_template
from flask import request
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')
@app.route("/prompt", methods = ['POST'])
def prompt():
    if request.method == 'POST':
        msg = request.form['prompt']
        return {"answer":msg}



