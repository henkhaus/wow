"""
takes guild from user list (wow.users) and finds 
members of each guild found, populating wow.users

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
posts = db.users
timestamp = time.time()

#create list of known users
print("Building known user lists from user database")
knownUsers = []
dbusers = posts.find()
for player in dbusers:
    
    username =(player['user'].split(" - ")[0])

    server = player['user'].split(" - ")[1]
    pid = player['user']
    try:
        playerinfo = wowapi.char_query(username,server)
        #print(guild)
        try:
            guild = playerinfo['guild']['name']
            print(guild)
        except: guild = "_None_"
        lvl = playerinfo['level']
        
        posts.update_one({'user':pid},{'$set':{'guild': guild, 'lvl':lvl, 'guildserver':playerinfo['guild']['realm']}})
        print("updated")
    except: print("Pass")



print("Known user list built")



    