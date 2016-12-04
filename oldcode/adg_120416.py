import pymongo
from pymongo import MongoClient
from wowlib import wowapi

client = MongoClient()

db = client.wow

#Variables
#call auction url script 
data = wowapi.auctionurl()


#set posts to auction data and insert into db
posts = db.auctiondata
posts.insert_many(data)




