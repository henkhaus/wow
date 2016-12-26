# Purpose: the script takes a unique list from the item collection to update the itemname field in the
# auctiondata collection
import pymongo
from pymongo import MongoClient
from wowlib import itemclasses as profile

# connection information
client = MongoClient("mongodb://76.31.221.129:27017/")

print('Initiating db connection and getting wow data')
db = client.wow
print("retrieved data")
posts = db.auctiondata
itemdb = db.items
#todo.* replace this flie with item_class_pipeline_query
# create list of known items and store in memory
item_cursor = itemdb.find()
item_list = []
for line in item_cursor:
    item_list.append(line)

# iterate through item list and update auctiondata wtih item class info
for row in item_list:
    x = row
    try:
        itemdata = profile.itemclass(row)
        classname = str(itemdata[0])
        subclass = str(itemdata[1])
        posts.update({'item': row['id'], 'itemname': "none defined"},
                     {'$set': {'itemname': row['name'],
                               'item_class': classname,
                               'item_subclass': subclass}}, multi=True)

    except Exception as e:
        posts.update({'item': row['id']}, {'$set': {'itemname': row['name']}}, multi=True)
        print(e)
