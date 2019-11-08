from flask import Blueprint, render_template
import map
import json
import pandas as pd
import math
import numpy
import sys

sys.path.insert(0, '/instagram/')
from instagram import instagram_crawling_methods

socialmedia = Blueprint('socialmedia', __name__)

@socialmedia.route("/social/reddit/count")
def reddit_count():
    csv_file = open('docs/toilet_Reddit_sentiments_3.csv')
    count =  sum(1 for line in csv_file) - 1
    results = {"count": count}
    return json.dumps(results)


@socialmedia.route("/social/instareview/count")
def instareview_count():
    csv_file = open('docs/username_post.csv')
    count =  sum(1 for line in csv_file) - 1
    results = {"count": count}
    return json.dumps(results)


@socialmedia.route("/insta/crawl/sadtoilet")
def crawl_sad_toilet():
    instagram_crawling_methods.get_csv_from_hashtag("sgsadtoilet")
    pd_read = pd.read_csv('docs/sgsadtoilet_post.csv') #iterate this weird way because Dataframe to CSV is flawed
    rows = pd_read.values.tolist()
    venue_dict = {"posts":[]}    

    for row in rows:
        
        display_url = row[7]
        location_name = row[31]

        if location_name != None and type(location_name) == str :
            poster_username = row[44]
            print(row[12])

            try: 
                caption = row[12].replace("[","").replace("]","")
                caption = caption.replace("\'","\"")
                caption_obj = json.loads(caption)

            except:
                caption_obj = {"node":{"text":""}}

            
            
            coord_dict = map.get_coords_by_name(location_name)
            print(coord_dict)
            foundObj = {
                "img_source": display_url,
                "location_name": location_name,
                "lat": coord_dict["lat"],
                "lon": coord_dict["lon"],
                "address": coord_dict["address"],
                "user_name": "@" + poster_username,
                "caption":caption_obj["node"]["text"]
            }
            venue_dict["posts"].append(foundObj)

    venue_dict["count"] = len(venue_dict["posts"])
    return json.dumps(venue_dict)


@socialmedia.route("/sgsadtoilet")
def show_sad_toilets():
    response = crawl_sad_toilet()
    hashtag_counts = json.loads(response)["count"]
    return render_template('sgsadtoilet.html',title='Sg Sad Toilet',jsonResponse=response,count=hashtag_counts)

