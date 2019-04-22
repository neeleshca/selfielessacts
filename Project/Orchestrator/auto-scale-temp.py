from flask import Flask
import threading
import time

import requests
import docker
import time


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
        b = client.containers.run('acts',ports={'80/tcp': int(samePort)},network="network1",environment={"TEAM_ID":"CC_208_222_223_236"},name=str(samePort)+"_acts",detach = True)
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

def autoScaler():
    global numberOfHTTPRequests
    global numberOfRunningContainers
    global portIds
    print("Starting auto scaler")
    client = docker.from_env()
    while(numberOfHTTPRequests == 0):
        pass
    while(True):
        print("number of http requests = "+str(numberOfHTTPRequests))
        newNumberOfContainers = int(numberOfHTTPRequests / 20) + 1
        print("number of containers = "+str(newNumberOfContainers))
        if(newNumberOfContainers > numberOfRunningContainers):
            print("starting "+str(newNumberOfContainers - numberOfRunningContainers)+" containers")
            print("Scaling up") # SCALE UP
            for i in range(0,newNumberOfContainers):
                if(str(8000+i) not in portIds):
                    b = client.containers.run('acts',ports={'80/tcp': 8000+i},network="network1",environment={"TEAM_ID":"CC_208_222_223_236"},name=str(8000+i)+"_acts",detach = True)
                    portIds[str(8000+i)] = b.id
            numberOfRunningContainers = newNumberOfContainers
        elif(newNumberOfContainers < numberOfRunningContainers):
            print("stopping "+str(numberOfRunningContainers - newNumberOfContainers)+" containers")
            print("Scaling down") #SCALE DOWN
            for i in range(numberOfRunningContainers-1,newNumberOfContainers-1,-1):
                a = client.containers.get(portIds[str(8000+i)])
                a.stop()
                a.remove()
                del portIds[str(8000+i)]
            numberOfRunningContainers = newNumberOfContainers
        else:
            print("Still the same")
        numberOfHTTPRequests = 0
        time.sleep(120)


def startOrchestrator():
    healthCheckThread = threading.Thread(target = healthCheck)
    autoScalerThread = threading.Thread(target = autoScaler)
    healthCheckThread.start()
    autoScalerThread.start()

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



@app.route('/api/v1/<route>', methods = ["GET", "POST", "DELETE"])
def handleRequest(route):
    global curr_container
    curr_container = (curr_container + 1) % numberOfRunningContainers
    path = "http://127.0.0.1:800" +  str(curr_container) + "/api/v1/" + str(route)
    print("Path:" + path)
    if request.method == "GET":
        resp = requests.get(url = path, json = request.get_json())
    elif request.method == "POST":
        resp = requests.post(url = path, json = request.get_json())
    else:
        resp = requests.delete(url = path)
    print(resp.content)
    if(len(resp.content)==0):
        return '',resp.status_code
    else:
        return jsonify(resp.get_json()),resp.status_code
startOrchestrator()
if __name__ == "__main__":
    app.run(debug = True)
