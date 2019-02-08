import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("database")
db = client["database"]
actList = db["acts"]
categoryCount = db["category"]
userlist = db["users"]


d = [
    {
        "act": {
            "actID": "1234",
            "username": "Naveen",
            "timestamp": "23-01-2019:11-01-12",
            "caption": "caption text",
            "upvotes": 25,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actID": "1235",
            "username": "B",
            "timestamp": "23-01-2019:11-01-12",
            "caption": "caption text",
            "upvotes": 5646,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actID": "1236",
            "username": "C",
            "timestamp": "23-01-2019:11-01-12",
            "caption": "caption text",
            "upvotes": 423,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Nature",
        }
    },
    {
        "act": {
            "actID": "1237",
            "username": "D",
            "timestamp": "23-01-2019:11-01-12",
            "caption": "caption text",
            "upvotes": 56,
            "imgb64": "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
            "category": "Humans",
        }
    },
]

x = actList.insert_many(d)

cat = [
    {"category": {"name": "Nature", "count": 100}},
    {"category": {"name": "Humans", "count": 50}},
    {"category": {"name": "Other", "count": 25}},
]
y = categoryCount.insert_many(cat)

users = [
	{"user":{"username":"Naveen", "password":"abcd"}},
	{"user":{"username":"Neelesh", "password":"efgh"}},
	{"user":{"username":"Nishant", "password":"ijkl"}},
	{"user":{"username":"Midhush", "password":"mnop"}}
]

z = userlist.insert_many(users)