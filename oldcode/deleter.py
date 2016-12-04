import pymongo
from pymongo import MongoClient
import os
import datetime
from bson.objectid import ObjectId

from wowlib import queries

# boilerplate setup code
client = MongoClient()
db = client.wow
posts = db.posts
collection = db.ah

# calculate 3 days ago
gen_time = datetime.datetime.now() - datetime.timedelta(days=3)
# create dummy object id to query against
dummy_id = ObjectId.from_datetime(gen_time)
# get all docs that are older then 3 days
to_delete = posts.find({'_id': {'$lt': dummy_id}})

resultcount = 0
ids = []
# get count and create ids list
for doc in to_delete:
    resultcount += 1
    ids.append(doc['_id'])    
print('number of docs to delete: '+str(resultcount))

# delete the docs in the ids list
for id in ids:
    try:
        posts.remove({'_id': ObjectId(id)})
    except e as Exception:
        print('docs not deleted. ' + str(e))
