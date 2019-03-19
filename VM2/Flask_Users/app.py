from flask import Flask, request, send_from_directory, jsonify, make_response
from inspect import getsourcefile
import os
from os.path import abspath
import random
import pymongo
import time
import base64
from flask_restful import reqparse, abort, Api, Resource
import json
import re
import datetime
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
user = db["users"]


app = Flask(__name__)
api = Api(app)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]



def validate_request(content, input_type, req_len):
    if isinstance(content, (input_type,)) == False:
        return False
    if len(content) != req_len:
        return False

class User_normal(Resource):
    # Adding an user - API 1
    def post(self):
        try:
            content = request.json
        except:
            return make_response(jsonify({}), 400)

        if validate_request(content, dict, 2) == False:
            return make_response(jsonify({}), 400)

        for i in content.keys():
            if i not in ['username', 'password']:
                return make_response(jsonify({}), 400)
        
        if (not(isinstance(content["username"], str))):
            return make_response(jsonify({}), 400)
        
        if (not(isinstance(content["password"], str))):
            return make_response(jsonify({}), 400)

        # user already existing case
        query = user.find_one({"user.username": content["username"]})
        if query is not None:
            return make_response(jsonify({}), 400)

        regex = re.compile("^[a-fA-F0-9]{40}$")
        if not (regex.match(content["password"])):
            return make_response(jsonify({}), 400)

        dict_temp = {
            "user": {"username": content["username"], "password": content["password"]}
        }
        user.insert_one(dict_temp)
        return make_response(jsonify({}), 201)

    # New API - User List
    def get(self):
        x = user.find({})
        userlist = []
        for i in x:
            userlist.append(i["user"]["username"])
        if (len(userlist) == 0):
            return make_response('', 204)
        return make_response(jsonify(userlist), 200)

    def head(self):
        return make_response(jsonify({}), 405)


class User_delete(Resource):
    # Adding an user - API 2
    # Removing an user - API 2
    def delete(self, del_arg):
        query = user.delete_one({"user.username": del_arg})
        # user does not exist to be deleted
        if query.deleted_count == 0:
            return make_response(jsonify({}), 400)
        return make_response(jsonify({}), 200)

    def head(self, del_arg):
        return make_response(jsonify({}), 405)


api.add_resource(User_normal, "/api/v1/users")
api.add_resource(User_delete,"/api/v1/users/<del_arg>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)