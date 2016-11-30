#!/bin/bash

zip -r publications.zip ./*

for fn in `cat function-names.txt`; do
    aws lambda update-function-code --function-name "$fn" --zip-file fileb://publications.zip
done

rm publications.zip

