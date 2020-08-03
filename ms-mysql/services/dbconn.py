import os
from pymongo import MongoClient
from bson.objectid import ObjectId

hostname = os.environ['DB_HOSTNAME']
user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
hostnameurl = hostname+":27017"

client = MongoClient(
    host = hostnameurl, # <-- IP and port go here
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username= user,
    password= password,
)

def get_all_collections():
    db = client.db_pruebas
    collections = db.connections.find()
    return collections

def get_on_collection(id):
    db = client.db_pruebas
    collection = db.connections.find_one({"processName": id })
    return collection

def new_documment(data):
    db = client.db_pruebas
    res = db.connections.insert(data)
    return res

def update_documment(filter, newvalues):
    db = client.db_pruebas
    res = db.connections.update_one(filter, newvalues)
    return res

def delete_documment(id):
    db = client.db_pruebas
    res = db.connections.delete_one({"_id": ObjectId(id)})
    return res