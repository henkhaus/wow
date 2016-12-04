import pymongo
from pymongo import MongoClient, UpdateOne
from wowlib import wowapi, binary_search
import time

client = MongoClient()

print ('Initiating db connection and getting wow data')
db = client.wowdoc
data = wowapi.auctionurl('Shadow-Council')
posts = db.auctiondata

#create counters
count = 0
time = time.time()

#create list for operations
operations = {}

#create bulk upsert
bulk = posts.initialize_ordered_bulk_op()

print("Connected")

#create list of disctinct auctions in memory
print("Creating Auction List")
auction_list = []
auctions = posts.find().distinct('auc')
for auction in auctions:
    auction_list.append(auction)
print("Auction List Created")
#Iterate through data returned from wowapi




for auction  in data:
    row = data[count]
    #create new json, this allows you to add data not returned from wowapi
    newrow = {'buyout': row['buyout'],
    'timeLeft': row['timeLeft'],
    'quantity': row['quantity'],
    'seed': row['seed'],
    'username': {'name':row['owner'], 'server':row['ownerRealm']},
    'owner': row['owner'],
    'item': row['item'],
    'rand': row['rand'],
    'bid': row['bid'],
    'context': row['context'],
    'auc': row['auc'],
    'ownerRealm': row['ownerRealm'],
    'viewtime': time,
    'timeupdated': time,
    'itemname': "-----<None Defined>-----",
    'status':"Active",
    'bidincrease': 'N',
    }
    count += 1
    operations[str(newrow['auc'])]=newrow


print("all auctions created in operations")
posts.insert_one(operations)
print ('new doc added')