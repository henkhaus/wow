"""
will merge into userguild

"""
import pymongo
from pymongo import MongoClient
from wowlib import wowapi



# connection informattion
client = MongoClient()
db = client.wow
userdb = db.users

# create list of unique guilds
guildlist = []
user_list = []
for guild in userdb.find({"user": {'$regex' : ".* - Blackwater Raiders.*"}}):
    if guild['guild'] in guildlist:
        pass
    elif guild['guild']=="_None_":
        pass
    else:
        guildlist.append(guild['guild'])

#print(len(guildlist))
count = 0
for guild in guildlist:
    try:
        record = wowapi.guild_query(guild,'Blackwater Raiders')
        try:
            for i, member in enumerate(record['members']):
                if 'spec' in record['members'][i]['character']:
                    user_list.append((record['members'][i]['character']['name']+" - "+record['members'][i]['character']['realm']))
                    user = (record['members'][i]['character']['name']+" - "+record['members'][i]['character']['realm'])
                
                    newuser = {'guild':guild,
                    'user':user,
                    'lvl':record['members'][i]['character']['level'],
                    'spec':record['members'][i]['character']['spec']['name'],
                    'class':record['members'][i]['character']['class'],
                    'gender':record['members'][i]['character']['gender'],
                    'role':record['members'][i]['character']['spec']['role'],
                    'side':record['side']
                    }
                
                    try:
                        #<----------------temp to reschema------------->
                        userdb.update({'user':user},
                                      {'$set':
                        {'user':user,
                        'lvl':newuser['lvl'],
                        'guild':guild,
                        'side':newuser['side'],
                        'gender':newuser['gender'],
                        'role':newuser['role'],
                        'class':newuser['class'],
                        'spec':newuser['spec']}},
                                      upsert=True)
                        print("added " +user)



                        '''
                        posts.update({'user':user},
                        {'$set':
                        {'user':user,
                        'lvl':newuser['lvl'],
                        'guild':guild,
                        'side':}},
                        upsert=True)
                        print("added " +user)
                '''
                    except:print("Failed on "+user)


        except Exception as e:
            print("failed API call "+ guild)
            print (e)
            print (user)
    except:print("Failed" + guild)

 #       print("Could not print :"+guild)
print ("Total Number of Users :" + str(len(user_list)))
#Output

#print('Number of distinct users :'+ str(numusers))    




















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
