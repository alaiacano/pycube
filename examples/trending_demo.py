import pycube, datetime, pymongo
from time import mktime
import numpy as np
    
def generate_trending_data(N = 1000):
    values = np.random.exponential(100, N)
    now = datetime.datetime.now()
    times = [now - datetime.timedelta(0, i) for i in xrange(N)]
    times = np.array([int(mktime(i.timetuple())) for i in times])
    
    return times, values

    
if __name__ == "__main__":

    trend = pycube.trending.TopEvents('actions', '48mp5l', 'act', update_duration=2)
    trend.run()