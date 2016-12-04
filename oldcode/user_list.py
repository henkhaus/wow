from wowlib import queries

from pymongo import MongoClient
import os

client = MongoClient()

# using wow.users
db = client.wow
posts = db.users

auctiondata = db.auctiondata

# need owner, realm, and owner+realm
users = []

usercount = 0
for name in auctiondata.distinct('owner'):#,{'owner':1, 'realm': 1}):
    usercount += 1
    users.append(name)
print(usercount)
'''
for name in users:
    for doc in auctiondata.find(name,{'owner':1, 'realm': 1})
    print 
'''