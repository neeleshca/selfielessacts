#!/usr/bin/env python3
from flask import Flask,request,jsonify
import threading
import time
import os
import requests
import docker
import time
import sys
from pprint import pprint
from start import xml_d,image_d,network_d
import copy

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
        a = list(i.attrs['NetworkSettings']['Ports'].values())
        if(a[0] is not None):
            a[0][0]['HostPort']
            portIds[int(a[0][0]['HostPort'])] = i.id

    while(True):
        #print("PortIds are ",portIds)
        for port in list(portIds):
            #print("Port is ",port)
            #print(port<=8009)
            #print("Bool is ",not(port>=8000 and port<=8009))
            if(not(port>=8000 and port<=8009)):
                continue
            #print("Port is ",port)
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

def startContainer(port_no,dict_i):
    global portIds
    client = docker.from_env()
    temp_dict = copy.deepcopy(dict_i['port'])
    if (temp_dict[list(temp_dict.keys())[0]] is not None):
        temp_dict[list(temp_dict.keys())[0]]=port_no
    print("temp dict is ",temp_dict)
    temp_name = copy.deepcopy(dict_i['name'])
    temp_name = temp_name + str(port_no)
    b = client.containers.run(dict_i['image'],ports=temp_dict,network=dict_i['network'],environment=dict_i['environment'],name = temp_name,
    detach=True)
    # b = client.containers.run('acts',ports={'80/tcp': int(port_no)},network="network1",environment={"TEAM_ID":"CC_208_222_223_236", "user_ip":str(user_ip)},name=str(port_no)+"_acts", detach = True)
    portIds[str(port_no)] = b.id

def stopContainer(portId):
    global portIds
    client = docker.from_env()
    a = client.containers.get(portIds[str(portId)])
    del portIds[str(portId)]
    a.stop()
    a.remove()

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
        if(port is None):
            pass
        elif(newNumberOfContainers > dict_i["numberOfRunningContainers"]):
            print("starting "+str(newNumberOfContainers - dict_i["numberOfRunningContainers"])+" containers")
            print("Scaling up") # SCALE UP
            for i in range(0,newNumberOfContainers):
                if((port+i) not in portIds):
                    startContainer(port+i,dict_i)
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


def startOrchestrator():
    healthCheckThread = threading.Thread(target = healthCheck)
    # autoScalerThread = threading.Thread(target = autoScaler)
    apiHandlerThread = threading.Thread(target = api_handle)
    for i in xml_d:
        autoScalerThread = threading.Thread(target = autoScaler,args=(i,)).start()
    healthCheckThread.start()
    # autoScalerThread.start()
    apiHandlerThread.start()


def api_handle():
    print("hello")   
    @app.route('/<path:path>', methods = ["GET", "POST", "DELETE"])
    def handleRequest(path):
        path = '/'+path
        min = -1
        for i in xml_d:
            temp = i['prefixurl']
            if path.find(temp,0,len(temp))==0 :
                print("Inside loop\n")
                print("min is ",i["min"])
                i["numberOfHTTPRequests"]+=1
                i["curr_container"] = (i["curr_container"] + 1) % i["numberOfRunningContainers"]
                min = i["min"]
                print("Current is ",i["curr_container"])
                print("Path is ",path)
                print("Port is ",str((list(i['port'].values())[0])))
                print(str((list(i['port'].values())[0]) is None))
                if(str((list(i['port'].values())[0]) is None)==True):
                    print("inside\n")
                    print("Value is ",str((list(i['port'].values())[0]) is None))
                    min = -1
                    break
                path = "http://127.0.0.1:" +  str((list(i['port'].values())[0])+ i["curr_container"]) + str(path)
                print("Min after loop is ",min)
                break
        
        print("Path is ",path)
        print("Min is ",min)
        if(min==-1):
            return '',405
        

        print("Path:" + path)
        # return path

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

    
startOrchestrator()
