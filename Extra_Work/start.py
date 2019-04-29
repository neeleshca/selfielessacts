import docker
import os
import sys
import copy
user_ip = "54.173.162.32"
from xml2 import xml_d,image_d,network_d

client = docker.from_env()
# client.networks.create("network1", driver="bridge")
for i in xml_d:
    for i1 in range(i['min']):
        temp_dict = copy.deepcopy(i['port'])
        if (temp_dict[list(temp_dict.keys())[0]] is not None):
            temp_dict[list(temp_dict.keys())[0]]+=i1
        temp_name = copy.deepcopy(i['name'])
        if(i1 > 0):
            temp_name = temp_name + str(i1)
        client.containers.run(i['image'],ports=temp_dict,network=i['network'],environment=i['environment'],name = temp_name,
        detach=True)

print("Over\n")
'''
client.containers.run('acts',ports={'80/tcp': 8001},network="network1",name="8001_acts",detach = True)
client.containers.run('acts',ports={'80/tcp': 8002},network="network1",name="8002_acts",detach = True)
'''
