import pymongo
from pymongo import MongoClient
from matplotlib import pyplot as plt
import datetime

client = MongoClient("mongodb://76.31.221.129:27017/")

db = client.wowtest
db2 = client.wow
auctions = db2.auctiondata
posts = db.items
#get the most recent returm
m = auctions.find().distinct('timeupdated')
maxtimestamp = max(m)
#print (maxtimestamp)


#Create list of items from item collection that match metal and ore category (7,7)
test1 = posts.aggregate([{'$match':{'itemClass':7,'itemSubClass':7}},{'$project':{'itemnum' :'$id'}}])


#iterate through list and out put grouped data (so far this total all items seen)
for item in test1:
    rows =auctions.aggregate([{'$match':{"item":item['itemnum'], 'timeupdated':maxtimestamp}},
        {'$group':{
        '_id':'$itemname',
        'available':{'$sum':'$quantity'},
        'numSellers':{'$addToSet':'$owner'}
        }}])
    for row in rows:
        print(row['_id']+" - " + str(row['available'])+ " - "+str(row['numSellers']))
