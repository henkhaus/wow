from wowlib import itemclasses as profile
import pymongo
from pymongo import MongoClient
import datetime
from wowlib import wowapi, queries

client = MongoClient("mongodb://76.31.221.129:27017/")

db = client.wow
auctions = db.auctiondata
items = db.items

# create date pipeline of all auctions with missing item info
pipeline = auctions.aggregate([{'$match': {'item_class': "none defined"}},
                               {'$project': {'item': '$item'}}])

# create a distinct set of item numbers from pipeline
missing_set = set([])
for obj in pipeline:
    missing_set.add(obj['item'])
print(len(missing_set))

# iterate through set
for i, item in enumerate(missing_set):
    itemdoc = items.find_one({'id': item})
    try:
        # this runs if the item does not exist in item collection. it will add it to the collection
        if itemdoc is None:
            itemdoc = wowapi.itemquery(item)
            items.insert_one(itemdoc)
    except Exception as e:
        print(e)
    if itemdoc is not None:
        # this runs if the item is in the item collection
        try:
            itemdata = profile.itemclass(itemdoc)
            print(itemdata)
            classname = str(itemdata[0])
            subclass = str(itemdata[1])
            auctions.update({'item': item}, {'$set': {'itemname': itemdoc['name'],
                                                      'item_class': classname,
                                                      'item_subclass': subclass}}, multi=True)

        except Exception as e:
            print(e)
            print(itemdoc['id'])
