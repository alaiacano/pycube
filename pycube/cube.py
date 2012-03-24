#! /usr/bin/env python
"""
This is a module with tools for putting streaming log data into cube.
"""
import sys, datetime, pymongo
from tiers import *
from config import *


def new_type(type_name):
    """
    Configures mongo for a new cube type.
    
    new_type("growth")
    
    Returns True if it worked, False if it failed.
    """
    events = "%s_events" % type_name
    metrics = "%s_metrics" % type_name
    try:
        DB_CONN.create_collection(events)
        events_coll = DB_CONN[events]
        events_coll.create_index('t')
        DB_CONN.create_collection(metrics, {'capped': True, 'size': 1e7, 'autoIndexId': True})
        metrics_coll = DB_CONN[metrics]
        metrics_coll.create_index([
            ("i", pymongo.ASCENDING),
            ("_id.e", pymongo.ASCENDING),
            ("_id.l", pymongo.ASCENDING),
            ("_id.t", pymongo.ASCENDING)
            ])
        metrics_coll.create_index([
            ("i", pymongo.ASCENDING),
            ("_id.l", pymongo.ASCENDING),
            ("_id.t", pymongo.ASCENDING)
            ])
    except:
        return False
    return True
    
    
def update_cube(type_name, data):
    """
    Updates the collection in cube. Pass this the data object only,
    and it will be correctly formatted and inserted into the database.
    
    The data dict should have a key called 'time'. If it doesn't the 
    current time will be sent into cube.
    
    Example:
    
    
    data = {
    'time'  : datetime.datetime(2012, 3 24)
    'count' : 40,
    'key'   : 'users'
    }
    update_cube('testcollection', data)
    """
    events = "%s_events" % type_name
    metrics = "%s_metrics" % type_name
    
    # make sure these collections exist
    assert (events in COLLECTIONS) and (metrics in COLLECTIONS)
    
    insert_dict = {}
    try:
        insert_dict['t'] = data['time']
        del(data['time'])
    except KeyError:
        insert_dict['t'] = datetime.datetime.now()
    
    # we must have a date format!
    assert type(insert_dict['t']).__name__ == 'datetime'
    
    insert_dict['d'] = data
    print events, insert_dict
    
    DB_CONN[events].insert(insert_dict)

def flush(flush_type, times=None):
    """
    flushes the collection. Ported from 
    https://github.com/square/cube/blob/master/lib/cube/server/event.js
    """
    flush_type += "_metrics"
    
    coll = DB_CONN[flush_type]
    for tier in TIERS:
        floor = TIERS[tier]['floor']
        coll.update(
            {
                'i' : False,
                '_id.l' : tier,
                '_id.t' : {
                    '$lte' : floor(datetime.datetime.now()),
                    }
            },
            {'$set' : {'i' : True}},
            invalidate = True,
            multi = True
        )
    

def parse_act_social(line):
    """
    Parses a line from the act_social log and returns an object
    with the values of interest.
    """
    ts, action, page, user_id, geo, lang, to_blog = line.strip().split("\t")
    strip_ascii = lambda x: unicode(x).encode('ascii','ignore')
    data = {
        'action': int(action),
        'page'  : page,
        'lang'  : lang,
        'to_blog' : int(to_blog),
        'time'  : datetime.datetime.fromtimestamp(int(ts))
    }
    try:
        data['user_id'] = int(user_id)
    except ValueError:
        data['user_id'] = -1
    try:
        data['geo'] = (lambda x: "XX~XX-XX" if x=="COUNTRY~CITY" else strip_ascii(x))(geo),
    except:
        print geo
    return data
    
    
def main():
    """
    Main.
    """
    new_type('follows')
    while 1:
        line = sys.stdin.readline().strip()
        if line.strip()=="":
            continue
        data = parse_act_social(line)
        if data['action'] == 1:
            update_cube('follows', data)
        
if __name__ == "__main__":
    main()