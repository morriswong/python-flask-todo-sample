# mongo.py

from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps 
from operator import itemgetter, attrgetter, methodcaller
import datetime
import unittest

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)

@app.route('/home', methods=['GET'])
def home():
  data = []
  for post in mongo.db.test.find():
    data.append(post)
  data = sorted(data, key=itemgetter('pub_date'), reverse=True)
  return render_template('index.html', result = data)

@app.route('/starred',methods = ['GET'])
def starred():
  data = []
  for post in mongo.db.test.find({'favStatus' : True}):
    data.append(post)
  data = sorted(data, key=itemgetter('pub_date'), reverse=True)
  return render_template('index.html', result = data)

@app.route('/add',methods = ['GET'])
def add_get():
  return render_template('add.html')

@app.route('/add',methods = ['POST'])
def add_post():
  title = request.form['title']
  content = request.form['content']
  obj = {
    'title': title, 
    'details': content, 
    'pub_date': datetime.datetime.utcnow(),
    'favStatus': False
  }
  record_id = mongo.db.test.insert(obj)
  return redirect(url_for('home'))

@app.route('/updateTo',methods = ['POST'])
def updateTo_post():
  objId = request.form['update']
  todo = mongo.db.test.find_one({"_id" : ObjectId(objId)})
  return render_template('update.html', result = todo)

@app.route('/updateConfirm',methods = ['POST'])
def updateConfirm_post():
  objId = request.form.get('id')
  title = request.form.get('title')
  content = request.form.get('details')
  mongo.db.test.update({ "_id" : ObjectId(objId)}, 
    {'$set': {
      'title': title, 
      'details': content
    }
  })
  return redirect(url_for('home'))

@app.route('/star', methods = ['GET'])
def star_get():
  return redirect(url_for('home'))

@app.route('/star', methods = ['POST'])
def star_post():
  objId = request.form['star']
  todo = mongo.db.test.find_one({"_id" : ObjectId(objId)})
  if todo['favStatus']:
    todo['favStatus'] = False
  else:
    todo['favStatus'] = True
  mongo.db.test.save(todo)
  return redirect(url_for('home'))

@app.route('/del',methods = ['POST'])
def delete_post():
  objId = request.form['del']
  result = mongo.db.test.delete_one({'_id': ObjectId(objId)})
  return redirect(url_for('home'))

@app.route('/searchResult',methods = ['POST'])
def search_post():
  data = []
  query = request.form['search']
  mongo.db.test.create_index([('title','text')])
  todo = mongo.db.test.find({"$text": {"$search": query}})
  for doc in todo:
    data.append(doc)
  return render_template('index.html', result = data)

if __name__ == '__main__':
  app.run(debug=True)