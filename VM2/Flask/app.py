from flask import Flask, request, send_from_directory, jsonify
from inspect import getsourcefile
import os
from os.path import abspath
import random
import pymongo
import time
import base64
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
app = Flask(__name__)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]

# def sorted_images(category):
#     #Sorts images in reverse chronological order of modified time

#     #Lists all the images
#     images = os.listdir(os.path.join(PATH, "static", "Categories", category))
#     #Gives the filename which can be used by flask (From static folder)
#     images = [os.path.join("Categories",category,file) for file in images]
#     images_time = [os.path.getmtime(os.path.join(PATH, "static", file)) for file in images]
#     sort_list = [list(a) for a in zip(images, images_time)]
#     sort_list = sorted(sort_list, reverse=True, key=lambda x: x[1])
#     images = [i[0] for i in sort_list]
#     return images

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route("/")
# def images():
#     images = sorted_images("Category_0")
#     return render_template("images.html", images=images)

# @app.route("/submitted", methods = ['POST'])
# def submitted():
#     file = request.files["file"]
#     category = request.form.get("category")
#     caption = request.form.get("caption")
#     print("category: ", category)
#     print("caption: ", caption)
#     target = os.path.join(PATH, "static", "Categories", category, caption)
#     file.save(target)   
#     return redirect("/")

# @app.route("/upload")
# def upload_page():
#     return render_template("upload_page.html")
# @app.route("/signup")
# def signup():
#     return render_template("signup.html")

# @app.route("/deleted", methods = ['POST'])
# def deleted():
#     filePath = request.form.get("Delete")
#     filePath = os.path.join(PATH, "static", filePath)

#     #print(filePath)
#     os.remove(filePath)
#     return redirect("/")

# # @app.route("/user/")
# @app.route("/<path:thepath>")
# def show_single_image(thepath):
#     temp = thepath.rsplit('/')[-1]
#     caption = temp.rsplit('.')[0]
#     # print(thepath)
#     return render_template("image_single.html", image=thepath, caption = caption)



# @app.route("/<category>")
# def category_fun(category):
#     # print("Category is ", category)
#     images = sorted_images(category)
#     return render_template("category.html", info=category, images=images)
# @app.route("/api/v1/acts/upvote", methods = ['POST'])
# def upvote():
#     body =  request.get_json()
#     query = db.acts.find_one({"act.actID":str(body[0])})
#     if query is None:
#         print("Act Does Not Exist!")
#         return jsonify({}), 400    
#     db.acts.update_one({"act.actID":str(body[0])}, {'$inc':{"act.upvotes":1}})
#     return jsonify({}), 200
    
'''
APIs START HERE!!!!!!
'''


def getNumberOfActs(categoryName):
    
    category = db.category.find_one({"category.name":categoryName}) #query for category

    if(category == None): #if category does not exist

        return -1
    
    number = category["category"]["count"] #get size from the returned dictionary
    
    return number

#get Acts given category

def getActs(categoryName):
    
    acts = db.acts.find({"act.category":categoryName}) #query for acts given the category
    
    return acts


@app.route("/api/v1/acts/<actID>", methods = ['DELETE'])
def removeAct(actID):
    query = db.acts.find_one({"act.actID":actID})
    if query is None:
        print("Act Does Not Exist!")
        return jsonify({}), 400 
    db.category.update_one({"category.name":query["act"]["category"]}, {'$inc':{"category.count":-1}})
    db.acts.delete_one({"act.actID":actID})
    return jsonify({}), 200
@app.route('/api/v1/acts', methods = ['POST'])
def uploadAct():
    body = request.get_json()
    query = db.acts.find_one({"act.actID":str(body["actId"])})
    if query is not None:
        print("ActID already Exists!")
        return jsonify({}), 400
    try:
        time.strptime(body["timestamp"],"%d-%m-%Y:%S-%M-%H")
    except:
        print("Timestamp format not correct!")
        return jsonify({}), 400
    print(body["username"])
    query = db.users.find_one({"user.username":body["username"]})
    if query is None:
        print("User does not exist!")
        return jsonify({}), 400
    try:
        base64.b64decode(body["imgB64"])
    except:
        print("Image not Base64 Encoded")
        return jsonify({}), 400
    if "upvotes" in body:
        print("No upvotes field is to be set!")
        return jsonify({}), 400
    query = db.category.find_one({"category.name":body["categoryName"]})
    if query is None:
        print("Category does not exist!")
        return jsonify({}), 400
    
    toInsert = {"act":{"actID":str(body["actId"]), "username":body["username"],"timestamp":body["timestamp"],
        "caption":body["caption"],"upvotes":0,"imgb64":body["imgB64"],"category":body["categoryName"]
    }}
    db.acts.insert_one(toInsert)
    db.category.update_one({"category.name":body["categoryName"]}, {'$inc':{"category.count":1}})
    return jsonify({}), 201
        

    
@app.route('/api/v1/uservalidate', methods = ['POST'])
def validate_user():
    body = request.get_json()
    query = db.users.find_one({"user.username":body["username"]})
    print(query)
    if query is None:
        return jsonify({}), 400
    if query["user"]["password"] != body["password"]:
        return jsonify({}), 400
    else:
        return jsonify({}), 201

@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def listActs(categoryName):
    
    startRange = request.args.get("start") #get start parameter
    
    endRange = request.args.get("end") #get end parameter
    
    number = getNumberOfActs(categoryName) #get number of acts of the given category
    
    if(number == -1):
        
        return jsonify({}), 405  #method not allowed if category does not exist
    
    if(number == 0):
        
        return jsonify({}), 204  #no content if no acts under existing category
    
    if(startRange == None and endRange == None):   #if API 6 
        
        if(number < 100):
            
            acts = getActs(categoryName)
            
            actsList = []
            
            for i in acts:
            
                i.pop("_id")   #remove the Mongo-DB's in-built ObjectId attribute
            
                i["act"]["timestamp"] = i["act"]["timestamp"].strftime("%Y-%m-%d %H:%M:%S") #convert timestamp to string for json conversion
            
                actsList.append(i)
            
            response = json.dumps(actsList)
            
            return response, 200
        
        else:
        
            return jsonify({}), 413  #if number of acts in the given category is > 100 (Payload too large)
    
    else: #if API 8
        startRange = int(startRange)
        
        endRange = int(endRange)
        
        if(endRange-startRange+1 > 100):
            
            return jsonify({}), 413  #payload to large - range > 100

        if(startRange < 1 or endRange > number): #if invalid range, method not allowed
            
            return jsonify({}), 405
        
        acts = getActs(categoryName).sort("act.timestamp",-1) #sort in descending order of timestamp (latest first)
        
        tempList = []
        
        actsList = []
        
        for i in acts: #since acts object is not indexable, create a tempList
            
            tempList.append(i)
        
        for i in range(startRange-1,endRange-1):
            
            tempList[i].pop("_id")
            
            tempList[i]["act"]["timestamp"] = tempList[i]["act"]["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            
            actsList.append(tempList[i])
        
        response = json.dumps(actsList)
        
        return response, 200


@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def getNumberOfActsGivenCategory(categoryName):
    
    number = getNumberOfActs(categoryName)
    
    if(number == -1):
    
        return jsonify({}), 405
    
    return jsonify({}), 200

    
if __name__ == "__main__":
    app.run()



