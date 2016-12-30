
def auctiondoc(row, timestamp):
    newrow = {'buyout': row['buyout'],
              'timeLeft': row['timeLeft'],
              'quantity': row['quantity'],
              'seed': row['seed'],
              'username': {'name': row['owner'],
                           'server': row['ownerRealm']},
              'owner': row['owner'],
              'item': row['item'],
              'rand': row['rand'],
              'bid': row['bid'],
              'context': row['context'],
              'auc': row['auc'],
              'ownerRealm': row['ownerRealm'],
              'viewtime': timestamp,
              'timeupdated': timestamp,
              'itemname': "none defined",
              'status': "Active",
              'bidincrease': 'N',
              'item_class': "<none defined>",
              'item_subclass': "<none defined>",
              'bidtrac': [(0, 0) for x in range(45)]
              }
    return newrow