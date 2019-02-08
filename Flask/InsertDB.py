import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("db")
db = client["db"]
actList = db["Acts"]


a = [
  { "_id": 2, "username": "Peter", "upvotes": 27},
  { "_id": 3, "username": "Amy", "upvotes": 652},
  { "_id": 4, "username": "Hannah", "upvotes": 21},
  { "_id": 5, "username": "Michael", "upvotes": 345},
  { "_id": 6, "username": "Sandy", "upvotes": 2},
  { "_id": 7, "username": "Betty", "upvotes": 1},
  { "_id": 8, "username": "Richard", "upvotes": 331},   
]

d = [
    {"1234":{"username":"Naveen","timestamp":"23-01-2019:11-01-12",
		   "caption":"caption text","upvotes":25,
		   "imgb64":"TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
           "category":"Nature"
		  }},
    {"1235":{"username":"B","timestamp":"23-01-2019:11-01-12",
		   "caption":"caption text","upvotes":5646,
		   "imgb64":"TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
           "category":"Nature"
		  }},
    {"1236":{"username":"C","timestamp":"23-01-2019:11-01-12",
		   "caption":"caption text","upvotes":423,
		   "imgb64":"TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
           "category":"Nature"
		  }},
    {"1237":{"username":"D","timestamp":"23-01-2019:11-01-12",
		   "caption":"caption text","upvotes":56,
		   "imgb64":"TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb",
           "category":"Human"
		  }}      
	]

x = actList.insert_many(d)

print(x.inserted_ids)