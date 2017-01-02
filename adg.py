
"""
grabs auction house data and populates it to 
wow.auctiondata

"""
from wowlib import wowapi, queries, log, mongoconnection, doctemplates
import time
import os

logname = os.path.splitext(__file__)[0]
data = wowapi.auctionurl('Shadow-Council')
posts = mongoconnection.auctionconnection()


def findhour(bidtrac):
    try:
        firstempty = bidtrac.index(['0,0'])
        return firstempty
    except:
        return 0


@log.log(logname)
def get_data():
    # create counters
    count = 0
    newcount = 0
    timestamp = time.time()
    updated =0
    update_stats = {}

    # create list of distinct auctions in memory
    auction_list = []
    auctions = posts.find({'status':'Active'}).distinct('auc')
    for auction in auctions:
        auction_list.append(auction)
    print("Auction List Created")

    # Iterate through data returned from wowapi
    for i, auction in enumerate(data):
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
                                       'bidtrac.'+str(first_empty)+'.0': newrow['bid'],
                                       'bidtrac.'+str(first_empty)+'.1': timestamp}})
                updated += 1
                update_stats = log.logdicts(update_return, update_stats)
            except Exception as e:
                update_return = posts.update({'auc': newrow['auc']},
                             {'$set':{'timeupdated': timestamp}})
                updated += 1
                update_stats = log.logdicts(update_return, update_stats)
                log.logging.error(e)
        else:
            # if auction was not found in auction list, auction is inserted into auctiondata
            posts.insert_one(newrow)
            newcount += 1
        count += 1

    return {'totalCount': count, 'totalUpdated': updated, "auction_list_length": len(data)}, update_stats
    
get_data()
queries.set_inactive()