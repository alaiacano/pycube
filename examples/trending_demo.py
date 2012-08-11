import pycube
   
if __name__ == "__main__":

    trend = pycube.trending.TopEvents('actions', '48mp5l', 'act', update_duration=2)
    trend.run()