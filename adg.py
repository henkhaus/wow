
"""
grabs auction house data and populates it to 
wow.auctiondata

"""
import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries, log
import time

logname = os.path.splitext(__file__)[0]

client = MongoClient()

print ('Initiating db connection and getting wow data')
db = client.wow
data = wowapi.auctionurl('Shadow-Council')
print("retrieved data")
posts = db.auctiondata



@log.log(logname)
def get_data():
    #create counters
    count = 0
    newcount = 0
    timestamp = time.time()
    updated =0
    print ("Connected")
    #create list of disctinct auctions in memory
    print ("Creating Auction List")
    auction_list = []
    auctions =posts.find().distinct('auc')
    for auction in auctions:
        auction_list.append(auction)
    print ("Auction List Created")
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
        'viewtime': timestamp,
        'timeupdated': timestamp,
        'itemname': "-----<None Defined>-----",
        'status':"Active",
        'bidincrease': 'N',
        'bidtrac':{str(x):(0,0) for x in range(48)}

        }
        #if statement to insure that only new data is added to the DB. 

        if queries.binary_search(auction_list,newrow['auc'])== True:
            posts.update_one({'auc':newrow['auc']},{'$set':{'timeupdated': timestamp}})
            updated +=1
            print (updated)
        else: 
            posts.insert_one(newrow)
            newcount +=1
            offset = 25-len(newrow['owner'])
            print ('New Auction Created by: '+newrow['owner'] + ' '*offset+ ' Total Count :'+ str(count) + "      New auction count : "+ str(newcount) )
        
        count +=1

get_data()


