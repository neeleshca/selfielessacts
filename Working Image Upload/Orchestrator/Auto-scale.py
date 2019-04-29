
from flask import Flask,request,jsonify
import threading
import time
import os
import requests
import docker
import time
import sys

user_ip = "54.173.162.32"

print(user_ip)
app = Flask(__name__)

portIds = dict()


numberOfHTTPRequests = 0
numberOfRunningContainers = 1
curr_container = -1


def healthCheck():
    global portIds
    def containerCreate(oldId, samePort):
        global portIds
        del portIds[samePort]
        a = client.containers.get(oldId)
        a.stop()
        a.remove()
        b = client.containers.run('acts',ports={'80/tcp': int(samePort)},network="network1",environment={"TEAM_ID":"CC_208_222_223_236","user_ip":str(user_ip)},name=str(samePort)+"_acts", detach = True)
        portIds[samePort] = b.id
        print("Removed identifier = "+str(oldId))
        print("New identifier = "+str(b.id))

    print("Start Health Check")
    client = docker.from_env()
    for i in client.containers.list():
        if(i.name[5:9] == "acts"):
            portIds[i.name[0:4]] = i.id
    while(True):
        for port in list(portIds):
            try:
                response = requests.get("http://127.0.0.1:" + str(port) + "/api/v1/_health")
                print(response)
                print(port)
            except:
                print("Error")
                print(portIds)
                continue
            if 'response' in locals() and response.status_code == 500:
                containerCreateThread = threading.Thread(target = containerCreate, args = (portIds[port], port))
                containerCreateThread.start()
        time.sleep(1) 

def startContainer(port_no):
    global portIds
    client = docker.from_env()
    b = client.containers.run('acts',ports={'80/tcp': int(port_no)},network="network1",environment={"TEAM_ID":"CC_208_222_223_236", "user_ip":str(user_ip)},name=str(port_no)+"_acts", detach = True)
    portIds[str(port_no)] = b.id

def stopContainer(portId):
    global portIds
    client = docker.from_env()
    a = client.containers.get(portIds[str(portId)])
    del portIds[str(portId)]
    a.stop()
    a.remove()

def autoScaler():
    global numberOfHTTPRequests
    global numberOfRunningContainers
    global portIds
    print("Starting auto scaler")
    client = docker.from_env()
    while(numberOfHTTPRequests == 0):
        pass
    while(True):
        time.sleep(120)
        print("number of http requests = "+str(numberOfHTTPRequests))
        newNumberOfContainers = int(numberOfHTTPRequests / 20) + 1
        print("number of containers = "+str(newNumberOfContainers))
        if(newNumberOfContainers > numberOfRunningContainers):
            print("starting "+str(newNumberOfContainers - numberOfRunningContainers)+" containers")
            print("Scaling up") # SCALE UP
            for i in range(0,newNumberOfContainers):
                if(str(8000+i) not in portIds):
                    startContainer(8000 + i)
            numberOfRunningContainers = newNumberOfContainers
        elif(newNumberOfContainers < numberOfRunningContainers):
            print("stopping "+str(numberOfRunningContainers - newNumberOfContainers)+" containers")
            print("Scaling down") #SCALE DOWN
            for i in range(numberOfRunningContainers-1,newNumberOfContainers-1,-1):
                stopContainer(8000+i)
            numberOfRunningContainers = newNumberOfContainers
        else:
            print("Still the same")
        numberOfHTTPRequests = 0


def startOrchestrator():
    healthCheckThread = threading.Thread(target = healthCheck)
    autoScalerThread = threading.Thread(target = autoScaler)
    apiHandlerThread = threading.Thread(target = api_handle)
    healthCheckThread.start()
    autoScalerThread.start()
    apiHandlerThread.start()

def api_handle():
    print("hello")   
    @app.route('/api/v1/<path:path>', methods = ["GET", "POST", "DELETE"])
    def handleRequest(path):
        global numberOfHTTPRequests
        numberOfHTTPRequests+=1
        global curr_container
        curr_container = (curr_container + 1) % numberOfRunningContainers
        print("Path is ",path)
        path = "http://127.0.0.1:800" +  str(curr_container) +"/api/v1/"+ str(path)
        print("Path:" + path)
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
    @app.route("/request1",methods=["GET"])
    def api1():
        global numberOfHTTPRequests
        numberOfHTTPRequests+=1
        print("Request 1") 
        return "Request 123"
    

    @app.route("/request2")
    def api2():
        global numberOfHTTPRequests
        numberOfHTTPRequests+=1
        return "Request 245"


    @app.route("/request3")
    def api3():
        global numberOfHTTPRequests
        numberOfHTTPRequests+=1
        return "Request 345"


    app.run()
startOrchestrator()
