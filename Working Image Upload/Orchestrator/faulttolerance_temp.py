import requests
import docker
import time

portIds = dict()

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

client = docker.from_env()

for i in client.containers.list():
    if (i.name[5:9] == "acts"):
        portIds[i.name[0:4]] = i.id

while (True):
    for port in list(portIds):
        try:
            response = requests.get("http://127.0.0.1:" + str(port) + "/api/v1/_health")
        except:
            continue
        # unhealthy container detected
        if 'response' in locals() and response.status_code == 500:
            containerCreateThread = threading.Thread(target = containerCreate, args = (portIds[port], port))
            containerCreateThread.start()
    time.sleep(1)


