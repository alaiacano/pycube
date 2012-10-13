import pycube
# import pycurl
import urllib2
import json
import re
import datetime

if __name__ == "__main__":

    cube = pycube.Cube()

    req = urllib2.Request('http://developer.usa.gov/1usagov')
    req.add_header('Accept', 'application/json')
    req.add_header("Content-type", "application/x-www-form-urlencoded")

    stream = urllib2.urlopen(req)

    for click in stream:
        print click
        # click = json.loads(click)

        # # skip the heartbeats
        # if '_heartbeat_' in click.keys():
        #     print '_heartbeat_'
        #     continue

        # try:
        #     domain = re.search(r'\.([^\.]+\.(gov|mil))', click['u']).group(1)
        # except:
        #     print click['u']
        #     continue

        # print domain

        # timestamp = datetime.datetime.fromtimestamp(int(click['t']))
        # timestamp += datetime.timedelta(hours=4)   # timezone issue to be fixed.

        # data = {
        #     'time': timestamp,
        #     'type': 'domains',
        #     'data': {
        #         'u': domain
        #     }
        # }
        # cube.update(data)
