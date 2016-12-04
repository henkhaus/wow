import pymongo
from pymongo import MongoClient
from wowlib import wowapi, binary_search
import time


#connection informattion
client = MongoClient()

print ('Initiating db connection')
db = client.wowtest
print("retrieved data")
posts = db.users
timestamp = time.time()

#create list of known users
print("Building known user lists from user database")
knownUsers = []
guilds = posts.find({'server':'Shadow Council'}).distinct('guild')
guild_list =[]

for guild in guilds:
    guild_list.append(guild)

print("Number of Unique Guilds :"+ str(len(guild_list)))

members = {}
for guild in guild_list:
    guildinfo = guild_query(guild, 'Shadow Council')

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