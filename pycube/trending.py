import numpy as np
SECOND = 1
MINUTE = SECOND * 60
HOUR   = MINUTE * 60
DAY    = HOUR * 24
MONTH  = DAY * 30

class Trending(object):
    def __init__(self, interval):
        """
        Looks for when a specific feature becomes trending
        """
        
        # DAY, MONTH, HOUR, etc.
        self.interval = interval
        
        # MA lengths
        self.N1 = 1000
        self.N2 = 10
        
        # MA arrays
        self.a1 = np.zeros(self.N1)
        self.a2 = np.zeros(self.N2)

        
    def _index(self, timestamp, N):
        """
        Calculates the index to update in a "circular" array.
        
        """
        return ((timestamp - timestamp%interval)/interval) % N

    def update(self, timestamp, value):
        """
        Adds a new point to the tracker.
        """
        # update indexes
        i1 = self._index(timestamp, self.N1)
        i2 = self._index(timestamp, self.N2)
            
        # update the arrays
        if self._index(timestamp-1, self.N1) == i1:
            self.a1[i1] += value
        else:
            self.a1[i1] = value

        if self._index(timestamp-1, self.N2) == i1:
            self.a1[i2] += value
        else:
            self.a1[i2] = value

        
    def is_trending(self):
        """
        Returns true if this thing is trending.
        """
        return (np.mean(self.a2)) > (np.mean(self.a1) + np.std(self.a1))
        # return (np.mean(self.a2) - np.std(self.a2)) > (np.mean(self.a1) + np.std(self.a1))
