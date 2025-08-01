def expand_cats(market):
    cats = market['category']
    del market['category']
    del market['exchange']
    market['category1'] = cats[0]
    market['category2'] = cats[1]
    market['category3'] = cats[2]
    return market