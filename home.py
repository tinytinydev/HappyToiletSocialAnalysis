from flask import Blueprint, render_template
import map

home = Blueprint('home', __name__)

@home.route("/index")
@home.route("/")
def index():
    csv_file = open('docs/toilet_Reddit_sentiments.csv')
    response = map.get_coords_with_location(csv_file)
    return render_template('index.html',title='Home',jsonResponse=response)