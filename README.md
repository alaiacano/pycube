# About

The [cube](https://github.com/square/cube/) project is awesome. I would like to create and update new boards with a really simple python call.

This project is pretty early in its development. So far I'm able to update the cube data as is described below. The main advantage so far is that you can do any pre-processing or pre-aggregating in python and then launch a new cube collection in a few lines of code.

My goal is to have the page update dynamically based on real time trends. We'll see how it goes. Everything described on the page so far is working for me. I'd love to get any feedback.

## Connecting to cube

First you need to get cube up and running. Follow the instructions [here](https://github.com/square/cube/wiki). For a simple example running on your local machine, you'll need to install everything they suggest, then run these commands:

    git clone https://github.com/square/cube.git
    cd cube
    npm install
    mongod &
    cat schema/schema-create.js | mongo
    node bin/collector.js &
    node bin/evaluator.js &

## Installing pycube

The only dependency that I know of is `pymongo`, which is available through `pip`.

    sudo pip install pymongo
    git clone git@github.com:alaiacano/pycube.git
    cd pycube
    sudo python setup.py install

## Creating a new `type`

Each mongodb collection is referred to as a `type`. If you have a log file of a specific action, you're going to need to tell cube about it. This will set up the collections that cube requires and set all of the right indexes.

    import pycube
    cube = pycube.Cube()             # the collector is running on 127.0.0.1 by default.
    cube.new_type('actions')
    
## Logging actions

Now you want to fill it in with some data. Inserting a new record should goes like this:

    action = {
        'time' : datetime.datetime.now(),
        'type' : 'actions',
        'data' : {
            'action_type' : 'follow',
            'action_source' : 'some_url',
        },
    }
    cube.update(action)

## Piping in lots of data

Check out the [demo.py](https://github.com/alaiacano/pycube/blob/master/demo.py) file. It simply parses a line from stdin, builds the data dict and updates cube. I've been sending data into cube like this:

    tail -f logfile | grep "optional filter" | ./demo.py

## Viewing the graphs

The page will be hosted on `http://localhost:1081/`. See https://github.com/square/cube/wiki/Queries for example queries.