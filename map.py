from flask import Blueprint, render_template
import csv
import json
import requests

mapscreen = Blueprint('map', __name__)


@mapscreen.route("/map")
def map():
    #return "Complete"
    csv_file = open('docs/SampleMsgwLocation.csv')
    get_coords_with_location(csv_file)
    return render_template('map.html',title='Map')


def get_coords_with_location(csv_file):
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0

    not_found = []

    one_map_api_url = "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&searchVal="

    for row in csv_reader:
        #Get all the row data for this row
        location = row[0]
        print(location)
        message = row[1]
        sentiment = row[2]
        sentiment_score = row[3]
        date = row[4]

        rowOneMapSearch = one_map_api_url + location
        response =  requests.get(rowOneMapSearch)
        results  =  json.loads(response.content.decode('utf-8'))

        if(results['found'] !=0):
            lat = float(results["results"][0]['LATITUDE'])
            lon = float(results["results"][0]['LONGITUDE'])
        else:
            not_found.append(location)

