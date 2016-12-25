# Purpose: the script takes a unique list from the item collection to update the itemname field in the
# auctiondata collection
import pymongo
from pymongo import MongoClient
from wowlib import itemclasses as profile

# connection information
client = MongoClient("mongodb://76.31.221.129:27017/")

print ('Initiating db connection and getting wow data')
db = client.wow
print("retrieved data")
posts = db.auctiondata
itemdb = db.items

# create list of known users
item_cursor = itemdb.find()
item_list = []
for line in item_cursor:
    item_list.append(line)
print("list created")
# aggregates user name and server name return is {_id:{username:"",server:""}}

count = 0
for row in item_list:
    x = row
    try:
        itemdata = profile.itemclass(row)
        print(itemdata)
        classname = str(itemdata[0])
        subclass = str(itemdata[1])
        posts.update({'item': row['id'], 'itemname':"none defined"},{'$set': {'itemname': row['name'],'item_class':classname,'item_subclass': subclass}}, multi=True)
        count +=1
        print(count)

    except Exception as e:
        print(e)
        posts.update({'item': row['id']}, {'$set': {'itemname': row['name']}}, multi=True)
        count += 1
        print("failed standard update")
