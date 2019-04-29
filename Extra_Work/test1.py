#!/usr/bin/env python3
from flask import Flask,request,jsonify,make_response
import threading
import time
import os
import requests
import time
import sys
from pprint import pprint
from xml2 import xml_d,image_d,network_d
# user_ip = "54.173.162.32"

# print(user_ip)
app = Flask(__name__)


portIds = dict()
portIds = {"8000":1}
print("New file\n")
pprint(xml_d)
pprint(image_d)
pprint(network_d)


def startOrchestrator():
    apiHandlerThread = threading.Thread(target = api_handle)
    apiHandlerThread.start()
    for i in xml_d:
        autoScalerThread = threading.Thread(target = autoScaler,args=(i,)).start()


def startContainer(port_no):
    print(port_no)
    print("Start\n")

def stopContainer(portId):
    print("Stop\n")



def autoScaler(dict_i):
    print("Starting auto scaler")
    while(dict_i["numberOfHTTPRequests"] == 0):
        pass
    
    while(True):
        print("Going to sleep\n")
        time.sleep(dict_i["time"])
        print("Slept\n")
        print("number of http requests = "+str(dict_i["numberOfHTTPRequests"]))
        newNumberOfContainers = int(dict_i["numberOfHTTPRequests"] / dict_i["numberofrequests"]) + 1
        print("New number is ",newNumberOfContainers)
        print("number of containers = "+str(newNumberOfContainers))
        port = list(dict_i['port'].values())[0]
        if(newNumberOfContainers > dict_i["numberOfRunningContainers"]):
            print("starting "+str(newNumberOfContainers - dict_i["numberOfRunningContainers"])+" containers")
            print("Scaling up") # SCALE UP
            for i in range(0,newNumberOfContainers):
                if(str(port+i) not in portIds):
                    startContainer(port+i)
            dict_i["numberOfRunningContainers"] = newNumberOfContainers
            
        elif(newNumberOfContainers < dict_i["numberOfRunningContainers"]):
            print("stopping "+str(dict_i["numberOfRunningContainers"] - newNumberOfContainers)+" containers")
            print("Scaling down") #SCALE DOWN
            for i in range(dict_i["numberOfRunningContainers"]-1,newNumberOfContainers-1,-1):
                stopContainer(port+i)
            dict_i["numberOfRunningContainers"] = newNumberOfContainers
        else:
            print("Still the same")
        dict_i["numberOfHTTPRequests"] = 0



def api_handle():
    print("hello")   
    @app.route('/<path:path>', methods = ["GET", "POST", "DELETE"])
    def handleRequest(path):
        path = '/'+path
        min = -1
        for i in xml_d:
            temp = i['prefixurl']
            if path.find(temp,0,len(temp))==0 :
                i["numberOfHTTPRequests"]+=1
                i["curr_container"] = (i["curr_container"] + 1) % i["numberOfRunningContainers"]
                min = i["min"]
                print("Current is ",i["curr_container"])
                path = "http://127.0.0.1:" +  str((list(i['port'].values())[0])+ i["curr_container"]) + str(path)
                break
        if(min==-1):
            return make_response(jsonify({}), 405)
        

        print("Path:" + path)
        return path

        if request.method == "GET":
            resp = requests.get(url = path)
        elif request.method == "POST":
            resp = requests.post(url = path, json = request.get_json())
        else:
            resp = requests.delete(url = path,  json = request.get_json())
        print(resp.content)
        if(len(resp.content)==0):
            return '',resp.status_code
        else:
            return jsonify(resp.json()),resp.status_code

    app.run()

def fun1(arg1):
    print(arg1)
    return 1
    
for i in range(5):
    autoScalerThread = threading.Thread(target = fun1,args=(i,)).start()


startOrchestrator()
