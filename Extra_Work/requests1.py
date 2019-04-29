import requests
import time

for i in range(50):
    r = requests.get('http://127.0.0.1:5000/api/v1/hello')

time.sleep(12)

for i in range(50):
    r = requests.get('http://127.0.0.1:5000/api/v1/hello')
