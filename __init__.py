from flask import Flask
from flask import render_template
from .home import home
from .map import mapscreen

app = Flask(__name__, static_url_path='', 
            static_folder='static',)
app.register_blueprint(home)
app.register_blueprint(mapscreen)