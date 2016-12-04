import pymongo
from pymongo import MongoClient
import os

client = MongoClient()

# using wow.auctiondata
db = client.wow
posts = db.auctiondata


def liros():
    '''finds all liros documents'''
    resultcount = 0
    for name in posts.find({'owner':'Liros'},
                            {'owner': 1, 'auc': 1, 'bid': 1}):
        print (name)
        resultcount += 1
    print(resultcount)

def count_docs():
    '''finds all documents'''
    resultcount = 0
    for doc in posts.find():
        resultcount += 1
    print(resultcount)

def player_auction():
    '''finds unique auction items for currently for sale by user'''
    player = raw_input("User Name :")
    resultcount = 0
    for name in posts.distinct('auc',{'owner':player}):
        print (name)
        resultcount += 1
    print(resultcount)

def countdocs():
    ''' a really fast way to count the number of documents'''
    print (posts.count())

def current_aucs():
    '''finds current auctions for a player'''
    '''
    # calculate 3 days ago
    gen_time = datetime.datetime.now() - datetime.timedelta(days=3)
    # create dummy object id to query against
    dummy_id = ObjectId.from_datetime(gen_time)
    # get all docs that are older then 3 days
    to_delete = posts.find({'_id': {'$lt': dummy_id}})
    '''
    #player = raw_input("User Name :")
    #print(posts.find_one({'owner':player}).sort({'_id':-1}))    

def binary_search(lst, item):
    alist = sorted(lst)
    first = 0
    last = len(alist)-1
    found = False

    while first <= last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found
    





#print(posts.find_one())
#print(resultcount)
