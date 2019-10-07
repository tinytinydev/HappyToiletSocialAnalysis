from flask import Flask 
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html',title='Home')

@app.route("/map")
def map():
    return render_template('map.html',title='Map')
    