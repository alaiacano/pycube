# About

The [cube](https://github.com/square/cube/) project is awesome for displaying aggregations of real-time data. I would like to create new "boards" with a really simple python call, and I want the boards to show the most interesting content in real time. An example could be trending tags/topics on a social network, and instead of just listing the tags it will display a graph of the tag's post frequency for the last minute/hour/day/whatever. 

## Connecting to cube

First you need to get cube up and running. Follow the instructions [here](https://github.com/square/cube/wiki). For a simple example running on your local machine, you'll need to install everything they suggest, then run these commands:

    git clone https://github.com/square/cube.git
    cd cube
    npm install
    mongod &
    node bin/collector.js &
    node bin/evaluator.js &

## Installing pycube

The only dependency that I know of is `pymongo`, which is available through `pip`.

    sudo pip install pymongo
    git clone git@github.com:alaiacano/pycube.git
    cd pycube
    sudo python setup.py install

## Creating a new `type`

Each mongodb collection is referred to as a `type`. A dashboard can have boards pulling data from multiple types, but I don't generally do that so we'll see how that plays out as this project makes progress. Once you launch the node and mongod processes, the actual code to get up and running is simple. 

    import pycube
    cube = pycube.Cube()             # the collector is running on 127.0.0.1 by default.
    cube.initalize()                 # set up all of cube's internal collections (collectd, etc)
    cube.new_type('actions')
    
## Logging actions

Now you want to fill it in with some data. Inserting a new record is easy:

    action = {
        'time' : datetime.datetime.now(),
        'type' : 'actions',
        'data' : {
            'action_type' : 'follow',
            'action_source' : 'some_url',
        },
    }
    cube.update(action)

The dict must have the keys 'type' (string) and 'data' (dict). The 'time' key is optional, and the current time stamp will be used if it is left out.

## Examples

Check out the [demo.py](https://github.com/alaiacano/pycube/blob/master/examples/demo.py) file. It just picks random actions and sends them to the collector. You can then go to the cube web interface and start creating boards. 

The [trending_demo.py](https://github.com/alaiacano/pycube/blob/master/examples/trending_demo.py) is still extremely experimental (aka "broken"), but the idea is that it is a second script that will run, and create/update a dashboard with graphs of trending data, where you can insert your own definition of "trending".

## Viewing the graphs

The page will be hosted on `http://localhost:1081/`. See https://github.com/square/cube/wiki/Queries for example queries. More on this later.