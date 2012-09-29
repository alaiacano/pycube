#!/bin/bash

mongod &

node cube/bin/evaluator.js &
node cube/bin/collector.js &