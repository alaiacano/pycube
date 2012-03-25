# About

The [cube](https://github.com/square/cube/) project is awesome. I would like to create and update new boards with python instead of node.

This project is **EXTREMELY** early in its development. Nothing works yet at all, but here's how I'd like it to flow:

## Connecting to cube

We'll probably need to know where mongodb and the cube `node` processes are running.

## Creating a new `type`

Each mongodb collection is referred to as a `type`. If you have a log file of a specific action, you're going to need to tell cube about it. I'd like that to work like this:

    import pycube
	cube = pycube.Cube()
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
	
# We'll see how it goes.