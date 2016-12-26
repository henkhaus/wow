#1st step in updateing user collection. this script grabs distinct user id's from auctiondata collection
#and get basic character information for the user collection. after this scrip runs, userguild.py needs to run

import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries
import time


#connection informattion
client = MongoClient()
wowdb = client.wow
seconddb = client.wow
auctiondb = seconddb.auctiondata
userdb = wowdb.users
timestamp = time.time()


#create list of known users
knownUsers = []
dbusers = userdb.distinct('user')
for player in dbusers:
    knownUsers.append(player)
    


#aggregates user name and server name return is {_id:{username:"",server:""}}
usersdata = auctiondb.aggregate([{'$group':
                                      {"_id":{'username': '$owner',
                                              'server' : '$ownerRealm'}}}])

#create more usable dictionary
userdict = {}
error_count = 0
for users in usersdata:
    print ("error Count :" + str(error_count))
    # character names only only unique per server, so server name was appended in order for this to act as a key
    c_name = str(users['_id']['username'])
    c_server = str(users['_id']['server'])
    character_name = str(c_name + " - " + c_server)
    #this is in try block due to ascii errors

#/todo/incorporate item_update_classes_pipeline model
    try:
        player ={'user':character_name, #/todo/this is a depricated function
                 'guild': "_None_",
                 'firstseen': timestamp,
                 'lastseen': timestamp,
                 'lvl': 000}

        if userdb.find({'name':c_name, 'realm': c_server}).count()>0:
            userdb.update_one({'user': player['user']},
                              {'$set':{'lastseen': timestamp}})
            print("updated existing record")
        else:
            print ('adding new player')
            new_player  = wowapi.char_query(c_name, c_server)
            userdb.insert_one(new_player)


            print("player added")
    except Exception as e:
        error_count += 1
        print("Error")
        print(e)
        pass


