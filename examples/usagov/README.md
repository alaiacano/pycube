# Tracking 1.usa.gov clicks

This example will find the trending top level domains from the 1.usa.gov click stream. 1.usa.gov is a public mirror of shortened bit.ly links.

There are three steps (two, really) to get up and running:

0. Launch the mongo and node processes required by cube
1. Start a python script to collect and parse the click stream
2. Start a second python script to determine the trending domains and update the dashboard.

## Parsing the stream

The clickstream is located at http://developer.usa.gov/1usagov and the data looks like this:

```{python}
{
    u'_heartbeat_': 1348951861
}

{
    u'a': u'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    u'al': u'en-us,en;q=0.5',
    u'c': u'US',
    u'cy': u'Arlington',
    u'g': u'PV7XRi',
    u'gr': u'VA',
    u'h': u'SR9UNn',
    u'hc': 1348671684,
    u'hh': u'wwpinc.org',
    u'l': u'wwpinc',
    u'll': [38.860001, -77.053299],
    u'nk': 0,
    u'r': u'http://www.facebook.com/',
    u't': 1348951865,
    u'tz': u'America/New_York',
    u'u': u'http://www.army.mil/article/87806/Working_dog_reunites_with_handler_during_bedside_hospital_visit/'
}
```

The `usagov_parse.py` file consumes the clickstream and feeds it into cube.