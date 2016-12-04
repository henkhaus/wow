from wowlib import queries

from pymongo import MongoClient
import os
import datetime
from bson.objectid import ObjectId

client = MongoClient()

# using wow.auctiondata
db = client.wow
posts = db.auctiondata


# begin stats
# get number of docs
coll = posts.count()

# get number of users
usercount = 0
for name in posts.distinct('owner'):
    usercount += 1

# number of auctions
auccount = 0
for name in posts.distinct('auc'):
    auccount += 1

# average
aucs_per_user = int(auccount)/int(usercount)

# get last hour 
#gen_time = datetime.datetime.now() - datetime.timedelta(hours=1)
gen_time = datetime.datetime(2016, 11, 9, 17)
    # create dummy object id to query against
dummy_id = ObjectId.from_datetime(gen_time)
#dummy_id = ObjectId('581fa52e936aa20f2e5b8a15')
    # get all docs that are older then 3 days
last_hour = posts.find({'_id': {'$gt': dummy_id}}).count()

# summary
print('total collection size: '+str(coll))
print('number of unique users: '+str(usercount))
print('auction count: ' +str(auccount))
print('auctions per user: '+str(aucs_per_user))
print('docs in the last hour: '+str(last_hour))
#print('gen time :' + str(gen_time))