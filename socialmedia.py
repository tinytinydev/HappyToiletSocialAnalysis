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
    csv_file.close()


    csv_file = open('docs/toiletsg_post.csv')
    count += sum(1 for line in csv_file) - 1
    results = {"count": count}
    return json.dumps(results)

@socialmedia.route("/insta/crawl/toiletsg")
def crawl_toilet_sg():
    instagram_crawling_methods.get_csv_from_hashtag("toiletsg")
    pd_read = pd.read_csv('docs/toiletsg_post.csv')
    rows = pd_read.values.tolist()

    columns = get_columns_dict(list(pd_read.columns))
    print("Checking columns")
    print(columns)
    venue_dict = {"posts":[]}    
    location_name = None

    for row in rows:
        display_url = row[columns['display_url']]
        print("Display url: " + display_url )
        print(row[columns['location']])

        if math.isnan(row[columns['location']]):
            locData = row[columns['location.address_json']]
            if type(locData) == str or not math.isnan(locData):
                locData.replace(",","\"")
                location_name = json.loads(locData)["zip_code"]
        else:
            location_name = row[columns['location']]

        if location_name != None and type(location_name) == str :
            poster_username = row[columns['owner.username']]

            try: 
                caption = row[columns['edge_media_to_caption.edges']].replace("[","").replace("]","")
                caption = caption.replace("\'","\"")
                caption_obj = json.loads(caption)

            except:
                caption_obj = {"node":{"text":""}}
            
            coord_dict = map.get_coords_by_name(location_name)
            if coord_dict != None:
                print("INSTA GET LOCATION FOR TOILETSG")
                print(location_name)
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
    

@socialmedia.route("/insta/crawl/sadtoilet")
def crawl_sad_toilet():
    instagram_crawling_methods.get_csv_from_hashtag("sgsadtoilet")
    pd_read = pd.read_csv('docs/sgsadtoilet_post.csv') #iterate this weird way because Dataframe to CSV is flawed
    rows = pd_read.values.tolist()

    columns = get_columns_dict(list(pd_read.columns))
    print("Checking columns")
    print(columns)
    venue_dict = {"posts":[]}    
    location_name = None

    for row in rows:
        display_url = row[columns['display_url']]
        print("Display url: " + display_url )

        if type(row[columns['location.name']]) != str:
            locData = row[columns['location.address_json']]
            if type(locData) == str or not math.isnan(locData):
                locData.replace(",","\"")
                location_name = json.loads(locData)["zip_code"]
        else:
            location_name = row[columns['location.name']]

        if location_name != None and type(location_name) == str :
            poster_username = row[columns['owner.username']]

            try: 
                caption = row[columns['edge_media_to_caption.edges']].replace("[","").replace("]","")
                caption = caption.replace("\'","\"")
                caption_obj = json.loads(caption)

            except:
                caption_obj = {"node":{"text":""}}
            
            coord_dict = map.get_coords_by_name(location_name)
            if coord_dict != None:
                print("INSTA GET LOCATION FOR TOILETSG")
                print(location_name)
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


def get_columns_dict(datal):
    diction = {}
    for i in range(0,len(datal)):
        diction[datal[i]] = i

    return diction