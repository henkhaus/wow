from wowlib import wowapi
from pymongo import MongoClient
import os

client = MongoClient()

#data = wowapi.char_query('liros', 'Shadow Council')

#Connect to test db and auction db
db = client.test
posts = db.users
db2 = client.wow
auctiondata = db2.auctiondata

#create auction data search cursor

cursor = auctiondata.find({}).distinct('owner')

#create users list
users=[]
#create list of users
usercount = 0
for auction in cursor:
    try:
        if (str(auction['owner']+auction['ownerRealm'])) in users:
            pass
        else: 
            users.append(auction['owner']+' '+auction['ownerRealm'])
            usercout +=1
            print (usercount)
    except:
        print ('                             Bad data')

#test code

count = 0
for item in users:
    count +=1
    print users[count]


print (data)