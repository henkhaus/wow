from wowlib import wowapi, queries, log, mongoconnection, doctemplates
import time
import os
import multiprocessing
#/todo rewrite updatefunction to be a map function. Ie when mapped, all items in iterable can have this function applied to them
logname = os.path.splitext(__file__)[0]
data = wowapi.auctionurl('Shadow-Council')
posts = mongoconnection.auctionconnection()
threads = 3
####
# create counters
count = 0
newcount = 0
timestamp = time.time()
updated = 0
update_stats = {}

# create list of distinct auctions in memory
auction_list = []
auctions = posts.find({'status': 'Active'}).distinct('auc')
for auction in auctions:
    auction_list.append(auction)
print("Auction List Created")
######
data_parser =[]
for item in data:
    data_parser.append(item)



def findhour(bidtrac):
    try:
        firstempty = bidtrac.index(['0,0'])
        return firstempty
    except:
        return 0



def updatefunction(auction):
    count = 0
    newcount = 0
    updated = 0

    # create new json, this allows you to add data not returned from wowapi
    newrow = doctemplates.auctiondoc(auction, timestamp)

    # if statement to ensure that only new data is added to the DB.
    if queries.binary_search(auction_list, newrow['auc']) is True:
        curr_auc = posts.find_one({"auc": newrow['auc']})
        try:
            # findhour finds the index of first empty bidtrac tuple
            first_empty = findhour(curr_auc['bidtrac'])
            update_return = posts.update({'auc': newrow['auc']},
                                         {'$set': {'timeupdated': timestamp,
                                                   'bidtrac.' + str(first_empty) + '.0': newrow['bid'],
                                                   'bidtrac.' + str(first_empty) + '.1': timestamp}})
            updated += 1
            #update_stats = log.logdicts(update_return)
        except Exception as e:
            update_return = posts.update({'auc': newrow['auc']},
                                         {'$set': {'timeupdated': timestamp}})
            updated += 1
            #update_stats = log.logdicts(update_return, update_stats)
            log.logging.error(e)
    else:
        # if auction was not found in auction list, auction is inserted into auctiondata
        posts.insert_one(newrow)
        newcount += 1
    count += 1

def mp_handler(data_parser):
    p = multiprocessing.Pool(threads)
    p.map(updatefunction, data_parser)

if __name__ == '__main__':
    print('name')
    mp_handler(data_parser)
