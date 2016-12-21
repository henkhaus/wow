#Purpose: the script takes a unique list from the item collection to update the itemname field in the
#   auctiondata collection
import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries
import time


#connection informattion
client = MongoClient()

print ('Initiating db connection and getting wow data')
db = client.wow
print("retrieved data")
posts = db.auctiondata
itemdb = db.items



#create list of known users
knownitems = []
dbitems = itemdb.distinct('id')
for item in dbitems:
    knownitems.append(item)
print (len(knownitems)) 


#aggregates user name and server name return is {_id:{username:"",server:""}}




count = 0
for item in knownitems:
    try:
            iname = itemdb.find_one({'id':item})
            posts.update({'item':item, itemname:"-----<None Defined>-----"},{'$set':{'itemname':iname['name']}}, multi= True)
            count +=1

            

    except: 
        print("somethings wrong!!!!")

print (count)