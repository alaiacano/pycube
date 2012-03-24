import time, datetime
def timestamp(date_obj):
    """
    Turns a date object into a timestamp.
    """
    return time.mktime(date_obj.timetuple())

SECOND = 1
SECOND20 = 20 * SECOND
MINUTE = 60 * SECOND
MINUTE5 = 5 * MINUTE
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY

TIERS = {}
for tier in [SECOND, SECOND20, MINUTE, MINUTE5, HOUR, DAY, WEEK, MONTH, YEAR]:
    TIERS[tier] = {
      'key': tier,
      'floor': lambda d : datetime.datetime.fromtimestamp(timestamp(d)-(timestamp(d) % tier)),
      'ceil': lambda d : datetime.datetime.fromtimestamp(timestamp(d)-(timestamp(d) % tier)) + datetime.timedelta(0, tier),
      'step': lambda d : d + datetime.timedelta(0, tier),
    }
