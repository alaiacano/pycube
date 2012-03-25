#! /usr/bin/env python
"""
This is a module with tools for putting streaming log data into cube.
"""

import datetime, pymongo
import os, json, re

class Cube(object):
        
    def __init__(self, host='127.0.0.1'):
        """
        A class for controlling the cube connection
        """
        self._host = host
        self._conn = pymongo.Connection(self._host).cube_development
        self._collections = self._conn.collection_names()

    def __del__(self):
        """
        Close the connections
        TODO
        """
        pass 
        
    def type_exists(self, type_name):
        """
        Checks if the current type exists and returns True/False
        
        cube = Cube()
        cube.type_exists('follows')
        
        TODO
        """
        pass
        
    def new_type(self, type_name):
        """
        Configures mongo for a new cube type.
    
        new_type("growth")
    
        Returns True if it worked, False if it failed.
        """
        events = "%s_events" % type_name
        metrics = "%s_metrics" % type_name
        try:
            self._conn.create_collection(events)
            events_coll = self._conn[events]
            events_coll.create_index('t')
            self._conn.create_collection(metrics, {'capped': True, 'size': 1e7, 'autoIndexId': True})
            metrics_coll = self._conn[metrics]
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
    
    def clear_type(self, type_name):
        """
        Clears the collections from mongo if they exist.
        
        TODO
        """
        pass
   
    def update(self, data):
        """
        Sends the request to cube.
        
        TODO: do this without using os.system, or hide the
        {"status":200} responses.
        """
        data = re.sub('"', '\\"', '['+json.dumps(data)+']')
        os.system('curl -X POST -d "%s" http://localhost:1080/1.0/event/put' % data)
