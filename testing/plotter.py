from pymongo import MongoClient
from matplotlib import pyplot as plt
import os
from datetime import datetime, date, time, timedelta

client = MongoClient()

# using wowtest.auctiondata
db = client.wowtest
posts = db.auctiondata

auctions = posts.find().limit(10)
#time.time() into datetime --->
#datetime.datetime.fromtimestamp('xxxx').strftime('%c')

def dt_to_timestamp(dt):
    #timestamp = (dt - datetime(1970, 1, 1).total_seconds())
    return (int(dt.strftime('%s')))


def getdata(num, quantum):
    valid = []
    today = datetime.combine(date.today(), time())
    for i in range(num+1):
        day = today - i*quantum
        gte = dt_to_timestamp(day)
        lt = dt_to_timestamp(day+quantum)
        time_query = {'$gte':gte, '$lt':lt}
        valid.insert(0, posts.find({'viewtime':time_query}).count())
    return valid

def format_date(x, n):
    today = datetime.combine(date.today(), time())
    day = today - timedelta(hours=n-x-1)
    return day.strftime('%m%d%H')


def plotbar(data, color):
    plt.bar(range(len(data)), data, align='center', color=color)


# run 
n = 48
val = getdata(n, timedelta(hours=1))
plotbar(val, '#4788d2')

plt.xticks(range(n), [format_date(i, n) for i in range(n)], size='small', rotation=90)
plt.grid(axis='y')

plt.show()




