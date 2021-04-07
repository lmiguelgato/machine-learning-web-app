# Machine Learning web app :bulb:
A cool web app for machine learning, using React.js to build the UI, and using Flask for the API.

Most of the processing is distributed across threads by a task queue ([Celery](https://docs.celeryproject.org/)), to obtain a more responsive UI. The broker used to mediate between clients and workers is a [Redis](https://redis.io/) database.

## Development setup :computer:

### API

Although completely redesigned, this project is inspired on some example code from [this project](https://github.com/jwhelland/flask-socketio-celery-example), which in turn is based on [this project](https://github.com/miguelgrinberg/flask-celery-example).

To setup the API, you must:

:zero: Create a Python 3.8 virtual environment and activate it.\
For example, run: `virtualenv -p python3.8 venv && source venv/bin/activate`

:one: Install the requirements:\
`pip install -r requirements.txt`

:two: Start a local Redis server.\
For example, if you are on Linux or Mac, execute `.api/run-redis.sh` to install and/or launch a private copy. If running this bash script for the first time, execution permission might be needed: `chmod +x run-redis.sh`

:three: Start a Celery worker (in another terminal instance) by running:\
`celery -A main.celery worker --loglevel=info -E`

:four: Start the Flask application (in another terminal instance) by running:\
`python main.py`

A development server for the API will be running on [http://localhost:5000](http://localhost:5000), and it will reload if you make edits.

#### Running tests :microscope:

This project uses [PyTest](https://docs.pytest.org/) for testing. Simply run `pytest` from `src/api` to run all tests.

### React app

Make sure you have [Node.js JavaScript runtime](https://nodejs.org/) and [Yarn package manager](https://yarnpkg.com/) installed. This web app was developed with Node.js v15.13.0 (that comes with `npm` 7.7.6), and Yarn 1.22.10.

To setup the web app for development, make sure you are on the project root directory.\
Then install all required Node.js modules by running `yarn install` inside `static/`

To run the app in the development mode, run `yarn start` inside `static/` which should automatically open the app in your default browser.\
Otherwise, manually open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

#### Running tests :microscope:

Launch the test runner in the interactive watch mode by running `yarn test` inside `static/`\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

## Deployment setup :rocket:

### API

The API, as well as Celery and Redis instances live in separate Docker containers, which can be built by running `make run` inside `docker/`

The API is served using [NGINX](https://nginx.org/) and [uWSGI](https://uwsgi-docs.readthedocs.io/), which are bundled and ready for deployment in the API container.

### React app

To build the app for production, run `yarn build`\
It correctly bundles React in production mode, optimizes the build for the best performance, and save these files in the `build` folder.

The build is minified and the filenames include the hashes.\
The app is ready to be deployed!

See the section about deployment from [Facebook's repository](https://facebook.github.io/create-react-app/docs/deployment) for more information.
