import requests
from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from inspect import getsourcefile
import os
from os.path import abspath

app = Flask(__name__)
api = Api(app)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]
container_count = 3
curr_container = -1
def addContainer():
    global container_count
    container_count += 1
def delContainer():
    global container_count
    container_count -= 1

@app.route('/api/v1/<route>', methods = ["GET", "POST", "DELETE"])
def handleRequest(route):
    print("called!")
    global curr_container
    curr_container = (curr_container + 1) % container_count
    path = "http://127.0.0.1:800" +  str(curr_container) + "/api/v1/" + str(route)
    print("Path:" + path)
    print("hi1")
    if request.method == "GET":
        resp = requests.get(url = path, json = request.get_json())
    elif request.method == "POST":
        resp = requests.post(url = path, json = request.get_json())
    else:
        resp = requests.delete(url = path)
    print("hi2")
    print(resp.content)
    if(len(resp.content)==0):
        return '',resp.status_code
    else:
        return jsonify(resp.get_json()),resp.status_code
@app.route('/')
def temp():
    return "hello world"
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
