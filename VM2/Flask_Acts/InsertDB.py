import pymongo
import time
import datetime
from datetime import datetime
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("database")
db = client["database"]
actList = db["acts"]
categoryCount = db["category"]
userList = db["users"]
l = [datetime.strptime("23-01-2019:11-01-12","%d-%m-%Y:%S-%M-%H"),datetime.strptime("24-01-2019:11-01-13","%d-%m-%Y:%S-%M-%H"),datetime.strptime("25-01-2019:11-01-14","%d-%m-%Y:%S-%M-%H"),datetime.strptime("26-01-2019:11-01-15","%d-%m-%Y:%S-%M-%H")]
print(l)
d = [
    {
        "act": {
            "actId": "0",
            "username": "Naveen",
            "timestamp": l[0],
            "caption": "caption text",
            "upvotes": 25,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actId": "3",
            "username": "C",
            "timestamp": l[0],
            "caption": "caption text",
            "upvotes": 423,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actId": "1",
            "username": "B",
            "timestamp": l[1],
            "caption": "caption text",
            "upvotes": 5646,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actId": "4",
            "username": "D",
            "timestamp": l[3],
            "caption": "caption text",
            "upvotes": 56,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Humans",
        }
    },
]

x = actList.insert_many(d)

cat = [
    {"category": {"name": "Nature", "count": 3}},
    {"category": {"name": "Humans", "count": 1}},
    {"category": {"name": "Other", "count": 200}},
    {"category": {"name": "ABC", "count": 100}},
]
y = categoryCount.insert_many(cat)


users = [
    {"user": {"username": "Naveen", "password": "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589"}},
    {"user": {"username": "Neelesh", "password": "poiu"}},
    {"user": {"username": "abc", "password": "peie"}},
]

z = userList.insert_many(users)
