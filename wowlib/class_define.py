"""
will merge into wowlib

"""

import pymongo
from pymongo import MongoClient
from wowlib import wowapi



#connection informattion
client = MongoClient()

print ('Initiating db connection')
db = client.wow
print("retrieved data")
posts = db.users

rolelist= [{
        "id": 3,
        "mask": 4,
        "powerType": "focus",
        "name": "Hunter"
    }, {
        "id": 4,
        "mask": 8,
        "powerType": "energy",
        "name": "Rogue"
    }, {
        "id": 1,
        "mask": 1,
        "powerType": "rage",
        "name": "Warrior"
    }, {
        "id": 2,
        "mask": 2,
        "powerType": "mana",
        "name": "Paladin"
    }, {
        "id": 7,
        "mask": 64,
        "powerType": "mana",
        "name": "Shaman"
    }, {
        "id": 8,
        "mask": 128,
        "powerType": "mana",
        "name": "Mage"
    }, {
        "id": 5,
        "mask": 16,
        "powerType": "mana",
        "name": "Priest"
    }, {
        "id": 6,
        "mask": 32,
        "powerType": "runic-power",
        "name": "Death Knight"
    }, {
        "id": 11,
        "mask": 1024,
        "powerType": "mana",
        "name": "Druid"
    }, {
        "id": 12,
        "mask": 2048,
        "powerType": "fury",
        "name": "Demon Hunter"
    }, {
        "id": 9,
        "mask": 256,
        "powerType": "mana",
        "name": "Warlock"
    }, {
        "id": 10,
        "mask": 512,
        "powerType": "energy",
        "name": "Monk"
    }, {

}]


#for pclass in rolelist:
#    try:
#        print (pclass['name'])
#        role = pclass['name']
#        for user in posts.find({"class":pclass['id']}):
#            #print(user)
#            posts.update_one({'_id':user['_id']}),({'$set':{'class':role}})
#    except:
#        print(pclass)



def defineclass(userdoc):
    for pclass in rolelist:
        if pclass['id'] == userdoc['class']:
            return pclass['name']
