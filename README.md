# publications-api
lambda functions for the publications app


To install requirements:
`pip install -t ./lib -r requirements.txt`.

To deploy the whole project for testing (only do this if you change serverless.yml):
`serverless deploy -v`.

To deploy a particular funtion (replace FUNCTION_NAME with the actual name):
`serverless deploy function -f FUNCTION_NAME -v`.

To test a function with input data, first deploy it, then run (replace FUNCTION_NAME with the actual name):
`serverless invoke -f FUNCTION_NAME -p test-events/FUNCTION_NAME.json -l`.
Note, you should edit/create test-events/FUNCTION_NAME.json for whatever function you want to test.
