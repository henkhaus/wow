#this script searches a distinct list of guilds from user collection. the return is then used to populate the
#user collection with the guild roster

import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries
import time


#connection informattion
client = MongoClient()
db = client.wowtest
posts = db.users
timestamp = time.time()
#/todo/ code requires manual server unput
#create list of known users
print("Building known user lists from user database")
knownUsers = []
guilds = db.find({'server':'Shadow Council'}).distinct('guild')
guild_list =[]

for guild in guilds:
    guild_list.append(guild)

print("Number of Unique Guilds :"+ str(len(guild_list)))

#create list of guild servers

members = {}
for guild in guild_list:
    guildinfo = wowapi.guild_query(guild, 'Shadow Council')

    record ={'server':guildinfo['realm'],
             'faction':guildinfo['side'],
             'members':guildinfo['members']
    }


    print(guild + " : "+ len(record['members']))


    
    




















'''   
    
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
        
        posts.update_one({'user':pid},{'$set':{'guild': guild, 'lvl':lvl}})
        print("updated")
    except: print("Pass")



print("Known user list built")



'''    
