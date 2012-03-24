#! /usr/bin/env python
"""
This is a module with tools for putting streaming log data into cube.
"""
import sys, datetime, pymongo
from tiers import *

HTTP_HOST = '127.0.0.1'
DB_CONN = pymongo.Connection(HTTP_HOST).cube_development
COLLECTIONS = DB_CONN.collection_names()


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

def flush(flush_type):
    """
    flushes the collection. Ported from the following JavaScript:
    // Invalidate cached metrics.
    endpoint.flush = function() {
      var types = [];
      for (var type in flushTypes) {
        var metrics = collection(type).metrics,
            times = flushTypes[type];
        types.push(type);
        for (var tier in tiers) {
          var floor = tiers[tier].floor;
          metrics.update({
            i: false,
            "_id.l": +tier,
            "_id.t": {
              $gte: floor(times[0]),
              $lte: floor(times[1])
            }
          }, invalidate, multi);
        }
      }
      if (types.length) util.log("flush " + types.join(", "));
      flushTypes = {};
    };

    flushInterval = setInterval(endpoint.flush, flushDelay);
    """
    coll = DB_CONN[flush_type]
    coll.update({
        'i' : False,
        '_id.l' : ,
    })
    

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
        # 'user_id' : (lambda x: int(x) if x != "GO_UUID" else -1)(user_id),
    }
    try:
        data['user_id'] = int(user_id)
    except ValueError:
        data['user_id'] = -1
    try:
        data['geo'] = (lambda x: "XX~XX-XX" if x=="COUNTRY~CITY" else strip_ascii(x))(geo)[0],
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