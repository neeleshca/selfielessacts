import requests
import time

for i in range(0,125):
	requests.get("http://ubuntu@ec2-3-94-6-89.compute-1.amazonaws.com:7000/request1")
	time.sleep(0.1)


for i in range(0,125):
	requests.get("http://ubuntu@ec2-3-94-6-89.compute-1.amazonaws.com:7000/request1")
	time.sleep(0.30)

for i in range(0,150):
	requests.get("http://ubuntu@ec2-3-94-6-89.compute-1.amazonaws.com:7000/request1")
	time.sleep(1)
