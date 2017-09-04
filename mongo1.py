# mongo1.py
from pprint import pprint
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017/')

# data base name : 'test-database-1'
mydb = client['test-database-1']

myrecord = {
        "author": "Mike",
        "title" : "PyMongo 202",
        "tags" : ["MongoDB", "PyMongo", "Tutorial"],
        "date" : datetime.datetime.utcnow()
        }

myrecord2 = [
        { "author": "Duke II",
          "title" : "PyMongo II 101",
          "tags" : ["MongoDB II", "PyMongo II", "Tutorial II"],
          "date" : datetime.datetime.utcnow() },
        { "author": "Duke III",
          "title" : "PyMongo III 101",
          "tags" : ["MongoDB III", "PyMongo III", "Tutorial III"],
          "date" : datetime.datetime.utcnow() }
        ]

# record_id = mydb.mytable.insert(myrecord2)

# print (record_id)
# print (mydb.collection_names())

print (mydb.mytable.count())

for post in mydb.mytable.find():
    pprint (post)