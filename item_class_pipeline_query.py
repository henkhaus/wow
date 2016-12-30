from wowlib import log, mongoconnection, itemclasses as profile
from wowlib import wowapi
import os

logname = os.path.splitext(__file__)[0]
auctions = mongoconnection.auctionconnection()
items = mongoconnection.itemsconnection()


@log.log(logname)
def item_class_update():
    error_count = 0
    new_items = 0
    update_set_count = 0
    update_stats = {}
    # create date pipeline of all auctions with missing item info
    pipeline = auctions.aggregate([{'$match': {'itemname': "none defined"}},
                                   {'$project': {'item': '$item'}}])

    # create a distinct set of item numbers from pipeline
    missing_set = set([])
    for obj in pipeline:
        missing_set.add(obj['item'])

    # iterate through set
    for i, item in enumerate(missing_set):
        itemdoc = items.find_one({'id': item})
        try:
            # this runs if the item does not exist in item collection. it will add it to the collection
            if itemdoc is None:
                itemdoc = wowapi.itemquery(item)
                items.insert_one(itemdoc)
                new_items += 1
        except Exception as e:
            log.logging.error(e)
            error_count += 1
        if itemdoc is not None:
            # this runs if the item is in the item collection
            try:
                itemdata = profile.itemclass(itemdoc)
                print(itemdata)
                classname = str(itemdata[0])
                subclass = str(itemdata[1])
                update_data = auctions.update({'item': item}, {'$set': {'itemname': itemdoc['name'],
                                                                        'item_class': classname,
                                                                        'item_subclass': subclass}}, multi=True)

                update_stats = log.logdicts(update_data, update_stats)
                update_set_count += 1

            except Exception as e:
                log.logging.error(e)
                log.logging.debug(itemdoc)
                error_count += 1
    # return is for logging purposes
    return {'missing_set_length': len(missing_set), 'new_items': new_items, 'update_set_count': update_set_count,
            'error_count': error_count, }, update_stats

item_class_update()
