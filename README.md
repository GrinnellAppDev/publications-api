# Publications Api
> The backend for the publications app.  Built for
> [AWS](https://aws.amazon.com/) with [Serverless](https://serverless.com/).

## Workflow Dependencies

You will need these setup on your machine to manage your workflow.

- [pip](https://pip.pypa.io/) (`brew install pip`)
- [yarn](https://yarnpkg.com/) (`brew install yarn`) or
  [npm](https://www.npmjs.com/) (`brew install npm`)
  - Note, the commands below will use `yarn`, but you can substitute in `npm`.
- [AWS CLI](https://aws.amazon.com/cli/) (`pip install awscli`)
  - Also needs to be [configured](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html).

## Workflow

### Install Library Dependencies
To install the dependencies and do initial setup: `yarn install`. You
should only need to do this when you first clone, when requirements.txt or
package.json is changed, or when you create a new stage for the api.

### Deploy Dev Stage
To make sure your work doesn't collide with anyone else's, you should create a
seperate development stage for yourself.  A stage name must contain only
lowercase letters.  For example Zander's dev stage is called `zander`.  In the
following commands replace `stagename` with the name of your dev stage.
To deploy the whole project for testing: `yarn run deploy -- stagename`.

### Test Functions
You should edit/create `test-events/function_name.json` for whatever function
you want to test. To test a function with that input data:
`yarn run func -- function_name stagename`.

### Export Documentation
To export documentation for a stage to swagger, run:
`yarn run swagger -- stagename`. The docs will be available at
`http://publications-docs.s3-website.us-east-2.amazonaws.com/?stage=stagename`
where you substitute in your stage name at the end of the URL.  Note that this
will also deploy that stage.

### Deploy Production
Be careful with this one, we should all probably talk before we use it.  The
production stage is called `production`, so just deploy there:
`yarn run deploy -- production`

### Using Serverless Directly
To run a serverless command run: `yarn sls -- command`.  Replace
`command` with the actual command you would pass to serverless.  You probably
won't need to do this though.
