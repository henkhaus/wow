import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries
import time


#connection informattion
client = MongoClient()

print ('Initiating db connection and getting wow data')
db = client.wowtest
print("retrieved data")
posts = db.auctiondata
userdb = db.users
timestamp = time.time()


#create list of known users
knownUsers = []
dbusers = userdb.distinct('user')
for player in dbusers:
    knownUsers.append(player)
    


#aggregates user name and server name return is {_id:{username:"",server:""}}
usersdata = posts.aggregate([{'$group':{"_id":{'username': '$username.name', 'server' : '$username.server'}}}])
#create more usable dicyionary
userdict = {}
for users in usersdata:
    cname = str(users['_id']['username'])+" - "+str(users['_id']['server'])
    try:
       
        print(cname)
        player ={'user':cname,
        'guild':"_None_",
        'firstseen':timestamp,
        'lastseen':timestamp,
        'lvl':000}

        if queries.binary_search(knownUsers,player['user'])== True:
            userdb.update_one({'user':player['user']},{'$set':{'lastseen': timestamp}})
            updated +=1
            print (updated)
        else: 
            print ('adding new player')
            userdb.insert_one(player)
            newcount +=1
    except: pass

