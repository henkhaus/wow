
"""
grabs auction house data and populates it to 
wow.auctiondata

"""
import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries, log
import time, os

logname = os.path.splitext(__file__)[0]

client = MongoClient()

print('Initiating db connection and getting wow data')
db = client.wow
data = wowapi.auctionurl('Shadow-Council')
print("retrieved data")
posts = db.auctiondata




def findhour(bidtrac):
    count = 0
    for i,item in enumerate(bidtrac):
        if item == [0,0]:
            return i
        count += 0
    return 0

@log.log(logname)
def get_data():
    # create counters
    count = 0
    newcount = 0
    timestamp = time.time()
    updated =0
    update_stats = {}
    # create list of distinct auctions in memory
    print ("Creating Auction List")
    auction_list = []
    auctions =posts.find().distinct('auc')
    for auction in auctions:
        auction_list.append(auction)
    print ("Auction List Created")

    # Iterate through data returned from wowapi
    for i, auction in enumerate(data):
        row = data[i]
        #create new json, this allows you to add data not returned from wowapi
        newrow = {'buyout': row['buyout'],
                  'timeLeft': row['timeLeft'],
                  'quantity': row['quantity'],
                  'seed': row['seed'],
                  'username': {'name':row['owner'],
                               'server':row['ownerRealm']},
                  'owner': row['owner'],
                  'item': row['item'],
                  'rand': row['rand'],
                  'bid': row['bid'],
                  'context': row['context'],
                  'auc': row['auc'],
                  'ownerRealm': row['ownerRealm'],
                  'viewtime': timestamp,
                  'timeupdated': timestamp,
                  'itemname': "none defined",
                  'status': "Active",
                  'bidincrease': 'N',
                  'item_class': "<none defined>",
                  'item_subclass':"<none defined>",
                  'bidtrac':[(0,0) for x in range(45)]
        }

        #if statement to insure that only new data is added to the DB.

        if queries.binary_search(auction_list,newrow['auc'])== True:
            curr_auc = posts.find_one({"auc":newrow['auc']})
            try:
                #findhour finds the index of first empty bidtrac tuple
                x = findhour(curr_auc['bidtrac'])
                update_return =posts.update({'auc':newrow['auc']},
                             {'$set':{'timeupdated': timestamp,
                                      'bidtrac.'+str(x)+'.0': newrow['bid'],
                                      'bidtrac.'+str(x)+'.1': timestamp}})
                updated +=1
                update_stats = log.logdicts(update_return, update_stats)
                # print (updated)
            except Exception as e:
                # x = findhour(curr_auc['bidtrac'])
                update_return = posts.update({'auc':newrow['auc']},
                             {'$set':{'timeupdated': timestamp}})
                updated +=1
                update_stats = log.logdicts(update_return, update_stats)
                print (e)
        else:
            # if auction was not found in auction list, auction is inserted into auctiondata
            update_return = posts.insert_one(newrow)
            update_stats = log.logdicts(update_return, update_stats)
            newcount +=1
            offset = 25-len(newrow['owner'])
            print ('New Auction Created by: '+newrow['owner'] + ' '*offset+ ' Total Count :'+ str(count) + "      New auction count : "+ str(newcount) )

        count +=1

    return {'totalCount': count, 'totalUpdated': updated, "auction_list_length": len(data)}, update_stats
    
get_data()


