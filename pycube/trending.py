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
        
        try:
            interval = int(interval)
        except ValueError:
            raise Exception('Interval must be numeric.')
        
        # DAY, MONTH, HOUR, etc.
        self._interval = interval
        
        # MA lengths
        self._N1 = 1000
        self._N2 = 10
        
        # MA arrays
        self._a1 = np.zeros(self._N1)
        self._a2 = np.zeros(self._N2)

        
    def _index(self, timestamp, N):
        """
        Calculates the index to update in a "circular" array.
        
        """
        return (1.*(timestamp - timestamp%self._interval)/self._interval) % N

    def update(self, timestamp, value):
        """
        Adds a new point to the tracker.
        """
        # update indexes
        i1 = self._index(timestamp, self._N1)
        i2 = self._index(timestamp, self._N2)
        # update the arrays
        if self._index(timestamp-1, self._N1) == i1:
            self._a1[i1] += value
        else:
            self._a1[i1] = value

        if self._index(timestamp-1, self._N2) == i1:
            self._a1[i2] += value
        else:
            self._a1[i2] = value

        
    def is_trending(self):
        """
        Returns true if this thing is trending.
        """
        return (np.mean(self._a2)) > (np.mean(self._a1) + np.std(self._a1))
        # return (np.mean(self._a2) - np.std(self._a2)) > (np.mean(self._a1) + np.std(self._a1))

    def get_arrays(self):
        return self._a1, self._a2
        
        
class HoltWinters(object):
    def __init__(self, alpha=.25, beta=.25, gamma=.25, cycle_length=100):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        
        self._l = cycle_length
        self._s = 1.
        self._b = 1.
        self._c = [1.] * self._l

        self.__total_points = 0
        self.__t = self._l - 1
    
    def update(self, xt):
        """
        Adds a new data point.
        """
        xt = float(xt)
        s_t_1 = self._s
        t_1 = self.__t
        self.__total_points += 1
        
        self.__t = (self.__t + 1) % self._l

        self._s = self._alpha * (xt/(self._c[t_1])) + \
                  (1-self._alpha) * (s_t_1 + self._b)

        if self.__total_points == self._l:
            self._b = (1./self._l) * (self._y)
        else:
            self._b = self._beta * (self._s - s_t_1) + (1-self._beta) * self._b
        
        self._c[self.__t] = max(self._gamma * xt / (1-self._gamma) * self._c[self.__t], .0001)
        
    def forecast(self, m):
        """
        Forcasted value m cycles into the future.
        """
        index = m % self._l
        return (self._s + m*self._b) * self._c[m % self._l]
        
    def status(self):
        """
        Returns a dict with all of the parameters
        """
        status = {
            's' : self._s,
            'b' : self._b,
            # 'c' : self._c,
            'index' : self.__t,
            'L' : self._l,
        }
        return status
        