
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

print ('Initiating db connection and getting wow data')
db = client.wow
data = wowapi.auctionurl('Shadow-Council')
print("retrieved data")
posts = db.auctiondata
#findhour is broken. bridtrac returns 
#{'15': [0, 0],
# '13': [0, 0], etc..}

#searches through the old bidtrac return and returns an index
def oldfindhour(bidtrac):
    print (bidtrac)
    counter = 0
    for item in bidtrac:
        if bidtrac[item]== [0,0]:
            
            print ('found it at index '+str(counter))
            return counter
            break
        #else:
         #  return 0
        counter += 1
        print ("       counter"+ str(counter))


def findhour(bidtrac):
    count = 0
    for i,item in enumerate(bidtrac):
        if item == [0,0]:
            return i
            break
        count +=0



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
        'bidtrac':[(0,0) for x in range(48)] #recently changed from dict odicts to list of dicts

        }
        #if statement to insure that only new data is added to the DB. 

        if queries.binary_search(auction_list,newrow['auc'])== True:
            curr_auc = posts.find_one({"auc":newrow['auc']})
            try:
                x = findhour(curr_auc['bidtrac'])
                posts.update({'auc':newrow['auc']},{'$set':{'timeupdated': timestamp,'bidtrac.'+str(x)+'.0': newrow['bid'],'bidtrac.'+str(x)+'.1': timestamp}})
                updated +=1
                print (updated)
            except:
                #x = findhour(curr_auc['bidtrac'])
                posts.update({'auc':newrow['auc']},{'$set':{'timeupdated': timestamp,}})
                updated +=1
                print (updated)
        else: 
            posts.insert_one(newrow)
            newcount +=1
            offset = 25-len(newrow['owner'])
            print ('New Auction Created by: '+newrow['owner'] + ' '*offset+ ' Total Count :'+ str(count) + "      New auction count : "+ str(newcount) )
        
        count +=1

get_data()


