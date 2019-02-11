import time
import random
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("database")
db = client["database"]
actList = db["acts"]
categoryCount = db["category"]
userList = db["users"]


users_l = ["Midhush", "Naveen", "Neelesh", "Nishant"]
category_l = [
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
]

category_l_dict = dict()
for i in category_l:
    category_l_dict[i] = 0

times = list()
#1000 unique times, change it if you want
sec = 0
for i in range(1000):
    times.append(
        time.strptime(
            (time.strftime("%d-%m-%Y:%S-%M-%H", time.localtime(time.time() + sec))),
            "%d-%m-%Y:%S-%M-%H",
        )
    )
    sec += 1

#500 entries, change it if you want
act_insert = list()
for i in range(500):
    category_rand = random.choice(category_l)
    category_l_dict[category_rand] += 1
    d_temp = {
        "act": {
            "actID": str(int(time.time() * 10 ** 10)),
            "username": random.choice(users_l),
            "timestamp": random.choice(times),
            "caption": "caption text",
            "upvotes": str(random.randint(1, 1001)),
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": category_rand,
        }
    }
    act_insert.append(d_temp)

actList.insert_many(act_insert)

category_insert = list()
for key, value in category_l_dict.items():
    d_temp = {"category": {"name": key, "count": value}}
    category_insert.append(d_temp)


categoryCount.insert_many(category_insert)

users = [
    {"user": {"username": "Naveen", "password": "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589"}},
    {"user": {"username": "Neelesh", "password": "poiu"}},
    {"user": {"username": "Midhush", "password": "peie"}},
    {"user": {"username": "Nishant", "password": "peie"}},
]

userList.insert(users)