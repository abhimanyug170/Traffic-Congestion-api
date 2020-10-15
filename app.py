from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import requests

# to handle CORS error
from flask_cors import CORS

# handle .env
from dotenv import load_dotenv
import os

# handle "_id" field from string
from bson.objectid import ObjectId
# import json

# import auxillary file
from congestion import get_signal_times


app = Flask(__name__)
CORS(app)
api = Api(app)

client = MongoClient(os.environ["MONGODB_URI"])
db = client["locationDB"]
junction = db["junction"]


class Junctions(Resource):
    # create
    def post(self):
        posted_data = request.get_json()

        result = junction.insert_one({
            "coordinate": posted_data["coordinate"],
            "roads": posted_data["roads"],
            "name": posted_data["name"]
        })

        return jsonify({
            "status": 200,
            "_id": str(result.inserted_id)
        })

    # read all
    # return array of jucntions o
    def get(self):
        junctions = junction.find()
        ret = []
        for jn in junctions:
            ret.append({
                "_id": str(jn["_id"]),
                "name": jn["name"],
                "coordinate": jn["coordinate"],
                "roads": jn["roads"]
            })

        return jsonify({
            "status": 200,
            "junctions": ret
        })
    

class GetTimer(Resource):
    # return timer values for all sides of a junction
    def get(self):
        _id = request.args.get("_id")
        index = int(request.args.get("index"))

        cur_junction = junction.find_one({
            "_id": ObjectId(_id)
        })

        if not cur_junction:
            return jsonify({
                "status": 404,
                "msg": "junction not found"
            })
        
        # make api request to distance-API
        key = os.environ["API_KEY"]
        url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
        source = ""
        for road in cur_junction["roads"]:
            source = source + str(road["lat"]) + "," + str(road["lon"]) + "|"
        
        params = {
            "origins": source[:-1],
            "destinations": str(cur_junction["coordinate"]["lat"]) + "," + str(cur_junction["coordinate"]["lon"]),
            "mode": "driving",
            "departure_time": "now",
            "traffic_model": "pessimistic",
            "key": key
        }
        
        # make api call
        response = requests.get(url, params=params).json()
        
        normal_times = [] 
        traffic_times = []
        
        for i in range(4):
            if i == index and index != -1:
                continue
            normal_times.append(response["rows"][i]["elements"][0]["duration"]["value"])
            traffic_times.append(response["rows"][i]["elements"][0]["duration_in_traffic"]["value"])
        
        # use algorithm
        signal_time, _ = get_signal_times(normal_times, traffic_times)
        if index != -1:
            signal_time.insert(index, 0)

        return jsonify({
            "signal_time": signal_time
        })


api.add_resource(Junctions, "/junctions")
api.add_resource(GetTimer, "/get-timer")

if __name__ == "__main__":
    app.run(port=5000)