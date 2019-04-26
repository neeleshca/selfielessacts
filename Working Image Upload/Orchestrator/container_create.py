import docker

client = docker.from_env()
client.networks.create("network1", driver="bridge")
client.containers.run('mongo:latest',network="network1",name="mongo_acts",detach = True)
client.containers.run('acts',ports={'80/tcp': 8000},network="network1",environment={"TEAM_ID":"CC_208_222_223_236"},name="8000_acts",detach = True)
client.containers.run('acts',ports={'80/tcp': 8001},network="network1",environment={"TEAM_ID":"CC_208_222_223_236"},name="8001_acts",detach = True)
client.containers.run('acts',ports={'80/tcp': 8002},network="network1",environment={"TEAM_ID":"CC_208_222_223_236"},name="8002_acts",detach = True)


