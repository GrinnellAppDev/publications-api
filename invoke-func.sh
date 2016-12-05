#!/bin/bash

serverless deploy function -f "$1" &&
serverless invoke -f "$1" -p "test-events/$1.json" -l
