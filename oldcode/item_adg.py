#this code takes a distinct list of item numbers from the item field in the auctiondata collection,
#and queries the wow api. The return from the wow api is inserted directly to the item collection


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
    


#aggregates user name and server name return is {_id:{username:"",server:""}}





for item in posts.find().distinct('item'):
    try:
        


        if queries.binary_search(knownitems,item)== True:

            print ("already seen")
        else: 
            newitem = wowapi.itemquery(item)
            #print ('adding new player')
            itemdb.insert_one(newitem)
            newcount +=1
    except: 
        print("failed on tryblock")

