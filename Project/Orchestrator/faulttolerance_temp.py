import requests
import docker
import time

portids = dict()
client = docker.from_env()

for i in client.containers.list():
    if (i.name[5:9] == "acts"):
        portids[i.name[0:4]] = i.id

while (True):
    for port, iden in portids.items():
        try:
            response = requests.get("http://127.0.0.1:" + str(port) + "/api/v1/_health")
        except:
            continue
        # unhealthy container detected
        if 'response' in locals() and response.status_code == 500:
            a = client.containers.get(iden)
            a.stop()
            a.remove()
            b = client.containers.run('acts',ports={'80/tcp': int(port)},environment={"TEAM_ID":"CC_208_222_223_236"},name=str(port)+"_acts",detach = True)
            portids[port] = b.id
            print("Removed identifier = " + str(iden))
            print("New identifier = " + str(b.id))
    time.sleep(1)


