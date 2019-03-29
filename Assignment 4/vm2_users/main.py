import os
import requests
from flask import Flask

app = Flask(__name__)

ip = http://users
@app.route('/')
def hello_world():
      r = requests.get(ip + '/')
      print(r.content)
      print("HELLO WORLD\n")
      html = "<h3>Hello {name}!</h3>"
      return html.format(name=r.content)

if __name__ == '__main__':
      app.run(host='0.0.0.0')
