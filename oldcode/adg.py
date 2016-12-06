import pymongo
from pymongo import MongoClient
import urllib2
import json

client = MongoClient()

db = client.wow
collection = db['ah']
# Variables
apikey = "8sv23p3ruq39kfng2phrrau3nstevp4j"
realm = "Shadow-Council"

# Build url for auction data requests


def buildurl(realm, key):
    base = "https://us.api.battle.net/wow/auction/data/"
    mid = "?locale=en_US&apikey="

    print(str(base + realm + mid + key))

    return str(base + realm + mid + key)


# grab header file
url = buildurl(realm, apikey)
req = urllib2.Request(url)
weburl = urllib2.urlopen(req).read()

encoding = weburl.decode('UTF-8')

data = json.loads(encoding)

# gather data from initial return
time = (data['files'][0]['lastModified'])
url = (data['files'][0]['url'])


# get auction data
req = urllib2.Request(url)
weburl = urllib2.urlopen(req).read()
encoding = weburl.decode('UTF-8')

data = json.loads(encoding)

posts = db.posts
posts.insert_many(data['auctions'])


result = 0
for post in posts:
    result += 1

print(result)
