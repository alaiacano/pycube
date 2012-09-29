import pycube
import urllib2
import json
import re

if __name__ == "__main__":

    cube = pycube.Cube()

    stream = urllib2.urlopen('http://developer.usa.gov/1usagov')

    for click in stream:
        click = json.loads(click)

        # skip the heartbeats
        if 'heartbeat' in click.keys():
            continue

        try:
            domain = re.search(r'\.([^\.]+\.(gov|mil))', click['u']).group(1)
        except:
            print click['u']
            continue

        timestamp = datetime.datetime.fromtimestamp(int(click['t'])) 
        timestamp += datetime.timedelta(hours=4)   # timezone issue to be fixed.

        data = {
            'time': timestamp,
            'data': {
                'u': domain
            }
        }
        cube.update(data)
