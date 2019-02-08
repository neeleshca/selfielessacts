import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("Database")
db = client["Database"]
actList = db["Acts"]
categoryCount = db["Category"]



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

cat = [
    {"Nature":100},
    {"Humans":50},
    {"Others":25}
]
y = categoryCount.insert_many(cat)