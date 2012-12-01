import pycube
import requests

if __name__ == "__main__":

    trend = pycube.trending.TopEvents(
        'usagov',
        '48mp5q',
        'd',
        update_duration=4,
        trend_duration=3900  # usagov data seems to be an hour behind
    )
    trend.run()
