#!/bin/bash

zip -r publications.zip ./*
aws lambda update-function-code --function-name post_article --zip-file fileb://publications.zip
rm publications.zip

