from flask import Flask
from flask import render_template
from .home import home
from .map import mapscreen

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(mapscreen)