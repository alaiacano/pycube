# About

The [cube](https://github.com/square/cube/) project is awesome. I would like to create and update new boards with python instead of node.

This project is **EXTREMELY** early in its development. Nothing works yet at all, but here's how I'd like it to flow:

## Connecting to cube

First you need to get cube up and running. Follow the instructions [here](https://github.com/square/cube/wiki). For a simple example running on your local machine, you'll need to install everything they suggest, then run these commands:

	cd cube
	mongod &
	node bin/collector.js &
	node bin/evaluator.js &

## Installing pycube

This is how it SHOULD work.

	sudo pip install pymongo
	git clone git@github.com:alaiacano/pycube.git
	cd pycube
	sudo python setup.py install
	
I just have to make `setup.py` still.

## Creating a new `type`

Each mongodb collection is referred to as a `type`. If you have a log file of a specific action, you're going to need to tell cube about it. I'd like that to work like this:

    import pycube
	cube = pycube.Cube()             # the collector is running on 127.0.0.1 by default.
	pycube.create_type('actions')
	
## Logging actions

Now you want to fill it in. Inserting a new record should go like this:

	action = {
		'time' : datetime.datetime.now(),
		'type' : 'actions',
		'data' : {
			'action_type' : 'follow',
			'action_source' : 'some_url',
		},
	}
	cube.update(action)
