#! /usr/bin/env python
import requests
import pycube
import json
import datetime
import re

if __name__ == "__main__":

    # Set up cube
    cube = pycube.Cube()
    board_name = 'usagov'

    cube.clear_type(board_name)
    cube.new_type(board_name)

    # Open the 1.usa.gov clickstream
    clickstream = requests.get(
        'http://developer.usa.gov/1usagov',
        prefetch=False
    )

    for click in clickstream.iter_lines():
        try:
            click = json.loads(click)
        except:
            continue
        if '_heartbeat_' in click.keys():
            continue

        # Extract the domain of the url
        click["d"] = re.sub('https?://.*\.(.+\.(gov|mil))(/.+)', '\\1', click['u'])

        # add to cube
        data = {
            'type' : board_name,
            'time' : datetime.datetime.fromtimestamp(click['hc']) + datetime.timedelta(hours=4),
            'data' : click
        }
        cube.update(data)

        print click['d']
