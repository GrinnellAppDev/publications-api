#!/bin/bash

serverless deploy function -f "$1" -s "${2:dev}" &&
serverless invoke -f "$1" -s "${2:dev}" -p "test/events/$1.json" -l
