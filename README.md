# Publications Api

> The web service for the publications app. Built with
> [Docker](https://docker.com/), [Node.js](https://nodejs.org/), and
> [MongoDB](https://mongodb.com/).

## Quick Start

Install [Docker](https://docs.docker.com/install/), then run
`./quickstart.sh`. The server will become available at
<http://localhost:4000>.

If you wish to use the "Try it Out" buttons to send requests to live servers,
be sure to select the appropriate server from the dropdown at the top.

## Workflow Dependencies

You will need these setup on your machine to manage your workflow.

- [yarn](https://yarnpkg.com/) (`brew install yarn`) or
  [npm](https://www.npmjs.com/) (`brew install npm`)
  - Note, the commands below will use `yarn`, but you can substitute in `npm`.
- [Docker](https://docs.docker.com/install/)

## Workflow

### Install Library Dependencies

To install the dependencies and do initial setup: `cd api` then, `yarn install`.
You should only need to do this when you first clone or package.json is
changed.

### Development Environment

With the dependencies installed, run `docker-compose up` from the project
root to start a development server. The api should be available at
<http://localhost:2000>.

When testing with the docs page, be sure to select the localhost server from
the dropdown.

### Production Environment

First, create a production configuration or copy the example file with
`cp docker-compose.prod.yml{.example,}`.

Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build`
to start a production server. Alternatively, run `./restart.sh` to run
production in the background. Either way, the production api will be
available at the port specified in the production configuration file.

### Deploying

When deploying on a server, ssh in, `git pull`, then run `./restart.sh` to
rebuild and restart the docker services.
