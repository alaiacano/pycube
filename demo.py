#! /usr/bin/env python
import pycube, sys, datetime

def parse_actions(line):
    """
    Parses a line from a log file and returns an object
    with the values of interest. I only want to record events
    where the second field of the log file is 1.
    """
    line = line.strip().split("\t")
    if line[1] != "1":
        return None
    data = {
        'time'  : (datetime.datetime.fromtimestamp(int(line[0]))+datetime.timedelta(0, 14400)).strftime("%Y-%m-%dT%H:%M:%S"),
        'data' : {
            'to' : int(line[6]),
        }
    }
    return data
    
def main():
    """
    Main.
    """
    cube = pycube.Cube()
    cube.new_type('follows')
    while 1:
        line = sys.stdin.readline().strip()
        if line.strip()=="":
            continue
        data = parse_actions(line)
        if data != None:
            data['type'] = 'follows'
            cube.update(data)

if __name__ == "__main__":
    main()