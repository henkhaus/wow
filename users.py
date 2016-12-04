"""

first pass: gathers users from wow.auctiondata
to populate wow.users

"""

import pymongo
from pymongo import MongoClient
from wowlib import wowapi, binary_search
import time


#connection informattion
client = MongoClient()

print ('Initiating db connection')
db = client.wow
print("retrieved data")
posts = db.auctiondata
userdb = db.users
timestamp = time.time()


#create list of known users
print("Building known user lists from user database")
knownUsers = []
dbusers = userdb.distinct('user')
for player in dbusers:
    knownUsers.append(player)
print("Known user list built")
    


#aggregates user name and server name return is {_id:{username:"",server:""}}
print("Aggregating auctiondata to build unique user list ")
usersdata = posts.aggregate([{'$group':{"_id":{'username': '$username.name', 'server' : '$username.server'}}}])
print("unique user list complete")
#create more usable dicyionary
print("user collection update started")
userdict = {}
count = 0
passcount = 0
for users in usersdata:
    
    try:
        cname = str(users['_id']['username'])+" - "+str(users['_id']['server'])
        player ={'user':cname,
        'guild':"_None_",
        'firstseen':timestamp,
        'lastseen':timestamp}

        if binary_search.binary_search(knownUsers,player['user'])== True:
            userdb.update_one({'user':player['user']},{'$set':{'lastseen': timestamp}})
        else: 
            userdb.insert_one(player)
            count +=1
    except: passcount +=1
print("User collection update complete")

print ("New users : "+str(count))
print ("errors : "+ str(passcount))
