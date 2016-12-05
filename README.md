# publications-api
lambda functions for the publications app

## Workflow Dependencies

You will need these setup on your machine to manage your workflow.

- [AWS CLI](https://aws.amazon.com/cli/) (pip install awscli)
  - Also needs to be [configured](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html).
- [Serverless](https://serverless.com/) (npm intstall -g serverless)

## Workflow

### Install Library Dependencies
To install the dependencies:
`pip install -t ./lib -r requirements.txt`.
You should only need to do this when requirements.txt is changed.

### Deploy Dev Stage
To deploy the whole project for testing (only do this if you change serverless.yml):
`serverless deploy -v`.

To deploy a particular funtion (replace FUNCTION_NAME with the actual name):
`serverless deploy function -f FUNCTION_NAME`.

### Test Functions
You should edit/create test-events/FUNCTION_NAME.json for whatever function you want to test.
To test a function with that input data, first deploy it, then run:
`serverless invoke -f FUNCTION_NAME -p test-events/FUNCTION_NAME.json -l`.

### Deploy Production
Be careful with this one, we should all probably talk before we use it:
`serverless deploy -s production -v`
