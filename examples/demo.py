#! /usr/bin/env python
import random, sys, datetime, time
import pycube

if __name__ == "__main__":
    cube = pycube.Cube()
    board_name = 'actions'
    cube.initialize_cube()
    if cube.type_exists(board_name):
        cube.clear_type(board_name)
    cube.new_type(board_name)
    
    action_types = ['post', 'like', 'follow', 'follow']

    current_time = datetime.datetime.now()
    for i in xrange(10000):
        data = {
            'type' : board_name,
            'time' : datetime.datetime.now() + datetime.timedelta(0, 4*3600),
            'data' : {
                'act' : random.sample(action_types, 1)[0]
            }
        }
        cube.update(data)
        time.sleep(.2)