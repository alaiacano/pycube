import numpy as np
import pymongo, random, time
SECOND = 1
MINUTE = SECOND * 60
HOUR   = MINUTE * 60
DAY    = HOUR * 24
MONTH  = DAY * 30

class TopEvents(object):
    """
    Updates a board with the top events.
    """
    def __init__(self, type_name, board_url, trend_variable, trend_duration = 60, update_duration = 10):
        """
        Creates a board with the given url.

        Inputs
        ------
        type_name : string
            The measurement type that you want to view. There should be another
            process populating this runnin elsewhere.
        board_url : string
            For now you have to provide a url TODO: fix this. important!
        trend_variable : string
            Variable name that you want to use as the trending value. For example,
            trend_variable should be "act" for the following input structure:

            data = {
                'type' : board_name,
                'time' : datetime.datetime.now() + datetime.timedelta(0, 4*3600),
                'data' : {
                    'act' : action_type
                }
            }

        Optional Inputs
        ---------------
        trend_duration : int
            Number of seconds of data to go through when considering what is trending.
        update_duration : int
            Number of seconds to wait between updating the board. Default is 10.

        """
        self.board_id = int(board_url.split("/")[-1], 36) # this is how cube does it.
        self.type_name = type_name
        self.board_url = board_url
        self.update_duration = update_duration
        self.host='127.0.0.1'
        self._conn = pymongo.Connection(self.host).cube_development
        self._build_board()


    def _build_board(self):
        """
        Creates a new board.
        """
        if self._conn.boards.find({'_id' : self.board_id}).count() > 0:
            raise Exception("The board %s already exists" % self.board_url)
        board_data = {'pieces' : []}

        self._conn.boards.insert(
            {'_id' : self.board_id},
            board_data
        )

    def run(self):
        """
        all testing so far
        """
        print "Your board is up and running at http://%s:1081/%s" % (self.host, self.board_url)

        # every 10 seconds:
        # * query for all unique events in the last minute
        # * get unique trend_variables
        # * aggregate and sort?
        # update the board with the top 4
        action_types = ['post', 'like', 'follow', 'follow']
        while 1:
            sum1, sum2 = random.sample(action_types, 2)
            pieces = [
                {
                    "id" : 1,
                    "query" : "sum(actions.eq(act,'%s'))" % sum1,
                    "time" : {
                        "range" : 1440000,
                        "step" : 20000
                    },
                    "position" : [
                        20,
                        3
                    ],
                    "type" : "sum",
                    "id" : 3,
                    "size" : [
                        8,
                        3
                    ]
                },
                {
                    "id" : 2,
                    "query" : "sum(actions.eq(act,'%s'))" % sum2,
                    "time" : {
                        "range" : 1440000,
                        "step" : 20000
                    },
                    "position" : [
                        10,
                        3
                    ],
                    "type" : "sum",
                    "id" : 3,
                    "size" : [
                        8,
                        3
                    ]
                },
                {   "id" : 3,   "size" : [  8,  3 ],    "position" : [  10,     0 ],    "type" : "text",    "content" : sum1 },
                {   "id" : 4,   "size" : [  8,  3 ],    "position" : [  20,     0 ],    "type" : "text",    "content" : sum2 }
            ]
            print pieces
            self._conn.boards.update(
                {'_id' : self.board_id},
                {'pieces' : pieces}
            )
            time.sleep(self.update_duration)



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
        