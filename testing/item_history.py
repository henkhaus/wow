from pymongo import MongoClient
from wowlib import wowapi, queries, log
import time, os


client = MongoClient()
db = client.wow
posts = db.auctiondata



