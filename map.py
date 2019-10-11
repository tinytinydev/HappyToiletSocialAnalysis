from flask import Blueprint, render_template
import csv
import json
import requests

mapscreen = Blueprint('map', __name__)


@mapscreen.route("/map")
def map():
    #return "Complete"
    csv_file = open('docs/SampleMsgwLocation.csv')
    response = get_coords_with_location(csv_file)
    print(response)
    return render_template('map.html',title='Map',jsonResponse=response)


@mapscreen.route("/")
def get_coords_with_location(csv_file):
    csv_reader = csv.reader(csv_file,delimiter=',')

    not_found = []
    successfulFound = []

    venueDict = {}

    one_map_api_url = "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&searchVal="

    next(csv_reader) #skip first line

    for row in csv_reader:
        #Get all the row data for this row
        location = row[0]
        message = row[1]
        sentiment = row[2]
        sentiment_score = row[3]
        date = row[4]

        if location not in venueDict.keys():
            rowOneMapSearch = one_map_api_url + location
            response =  requests.get(rowOneMapSearch)
            results  =  json.loads(response.content.decode('utf-8'))


            if(results['found'] !=0):
                lat = float(results["results"][0]['LATITUDE'])
                lon = float(results["results"][0]['LONGITUDE'])
                address = results["results"][0]['ADDRESS']
                foundObj =  {   
                                "location" : location,
                                "address" : address,
                                "messages" : [{
                                    "sentiment": sentiment,
                                    "message": message,
                                    "sentiment_score" : sentiment_score,
                                    "date": date,
                                }],
                                "lat" : lat,
                                "lon" : lon
                            }
                venueDict[location] = foundObj
            else:
                not_found.append(location)
        else: 
            foundObj = venueDict[location]
            foundObj["messages"].append({
                "sentiment": sentiment,
                "message": message,
                "sentiment_score" : sentiment_score,
                "date": date
            })

    for key in venueDict.keys():
        successfulFound.append(venueDict[key])
    searchJsonResponse =    {
                                "successful": successfulFound,
                                "unsuccessful" : not_found
                            }
    print (json.dumps(searchJsonResponse))
    return json.dumps(searchJsonResponse)