from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

# to handle CORS error
from flask_cors import CORS

# handle .env
from dotenv import load_dotenv
import os

# handle "_id" field from string
from bson.objectid import ObjectId


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
            "roads": posted_data["roads"]
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
                "coordinate": jn["coordinate"],
                "roads": jn["roads"]
            })

        return jsonify({
            "status": 200,
            "junctions": ret
        })
    

class GetTimer(Resource):
    # return timer values for all sides of a junction
    def get(self, _id):
        cur_junction = junction.find_one({
            "_id": ObjectId(_id)
        })

        if not cur_junction:
            return jsonify({
                "status": 404,
                "msg": "junction not found"
            })
        
        return jsonify({
            "status": 201,
            "msg": "test message"
        })


api.add_resource(Junctions, "/junctions")
api.add_resource(GetTimer, "/get-timer/<_id>")

if __name__ == "__main__":
    app.run(port=5000)