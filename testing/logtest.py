import pymongo
from pymongo import MongoClient
from wowlib import wowapi, queries, log
import time, os

logname = os.path.splitext(__file__)[0]

client = MongoClient("mongodb://76.31.221.129:27017/")

print('Initiating db connection and getting wow data')
db = client.wow
auction = db.auctiondata

@log.log(logname)
def logarguments():
    update_stats = {'n': 0, 'nModified': 0}
    update_return = {'n': 1, 'nModified': 20}
    update_stats = log.updatedict(update_return,update_stats)
    return {'one':1, 'two':2}, update_stats

logarguments()