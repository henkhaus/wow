from wowlib import mongoconnection


auctions = mongoconnection.auctionconnection()


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


def set_inactive():
    hour_list = auctions.find().distinct('timeupdated')
    hour_list = sorted(hour_list)
    last_seen = hour_list[-1]
    auctions.update({'timeupdated': {'$lt': last_seen}},
                    {'$set': {'status': 'inactive'}}, multi=True)
    return 0


def active_subclass_return(subclass_name: str) -> object:
    '''
    returns pipeline for selected sub_class contain current quantities and average costs
    :rtype: pipeline
    '''

    pipeline = auctions.aggregate([

        {'$match': {'status': 'Active', 'item_subclass':subclass_name}},
        {'$group': {
            '_id': '$itemname',
            'quantity': {'$sum': '$quantity'},
            'buyout': {'$avg': {'$divide': [{'$divide': ['$buyout', '$quantity']}, 10000]}}}},

    ])
    return pipeline
