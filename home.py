from flask import Blueprint, render_template
import map
import json
import socialmedia

home = Blueprint('home', __name__)

@home.route("/index")
@home.route("/")
def index():
    csv_file = open('docs/toilet_Reddit_sentiments_3.csv')
    response = map.get_coords_with_location_reddit(csv_file)

    #Social media counts
    reddit_count = json.loads(socialmedia.reddit_count())["count"]
    instareview_count = json.loads(socialmedia.instareview_count())["count"]



    return render_template('index.html',title='Home',jsonResponse=response,reddit_count=reddit_count,instareview_count=instareview_count)