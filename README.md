# Publications Api
> The backend for the publications app.  Built for [AWS](https://aws.amazon.com/)
> with [Serverless](https://serverless.com/).

## Workflow Dependencies

You will need these setup on your machine to manage your workflow.

- [AWS CLI](https://aws.amazon.com/cli/) (`pip install awscli`)
  - Also needs to be [configured](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html).
- [Serverless](https://serverless.com/) (`npm install -g serverless`)

## Workflow

### Install Library Dependencies
To install the dependencies: `pip install -t ./lib -r requirements.txt`. You
should only need to do this when you first clone or when requirements.txt is
changed.

### Deploy Dev Stage
To make sure your work doesn't collide with anyone else's, you should create a
seperate development stage for yourself.  A stage name must contain only
lowercase letters.  For example Zander's dev stage is called `zander`.  In the
following commands replace `stagename` with the name of your dev stage.
To deploy the whole project for testing: `serverless deploy -v -s stagename`. Only do this
if you change serverless.yml.

To deploy a particular funtion:
`serverless deploy function -f function_name -s stagename`.  Replace
`function_name` with the actual name.

### Test Functions
You should edit/create `test-events/function_name.json` for whatever function
you want to test. To test a function with that input data, first deploy it, then
run:
`serverless invoke -f function_name -p test/events/function_name.json -l -s stagename`.

Or, use the shortcut: `./invoke-func.sh function_name stagename`.

### Deploy Production
Be careful with this one, we should all probably talk before we use it.  The
production stage is called `production`, so just deploy there:
`serverless deploy -v -s production`
