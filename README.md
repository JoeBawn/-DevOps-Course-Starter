# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```


## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The `.env` file is also used to store credentials ensuring they are kept secret. 

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App in a Container using Docker

A Docker file has been created with configuration for both Production and Development environments. The app can be accessed from a browser at http://127.0.0.1:5000/ for any of the containers that are run

Run the below commands from the root directory to build and launch the app in production mode:
 
```bash
$ docker build --tag todo-app:production --target production .
$ docker run -d -p 5000:5000 --env-file .env todo-app:production 
```
Run the below commands from the root directory to build and launch in development mode:

```bash 
$ docker build --tag todo-app:development --target development .
$ docker run -d -p 5000:5000 --env-file .env --mount type=bind,source="$(pwd)"/todo_app,target=/temp/todo_app todo-app:development
```

## Heroku

This To-Do app is now hosted on Heroku:

https://todoapp-jb.herokuapp.com/

## Travis CI

This application is now deployed using Travis CI. Travis Builds are run on pull requests and include the the below tests in the 'Testing' section which are required to pass in order to deploy the application. 

## MongoDB

We are now using MongoDB in place of Trello. In order to configure this application to work with MongoDB you will need to update the following variables with the .env file:

MONGO_URL=[Your Connection String Here]
MONGO_DB_NAME=[Your DB Name Here]


## Testing

### Unit Tests

In order to run the unit tests, you will first need to ensure you have installed Pytest. You can find the suite of tests within todo_app/Tests/
Further details of the Pytest dependency can be found here: https://pypi.org/project/pytest/

The test_items.py file contains a card_list (list) contating several TrelloCard (objects) and trello_list_ids (dictionary) with an ID of each list used with the app for todo, inprogress and completed lists. 

You can run the tests from the directory using poetry run pytest

### E2E Tests
In order to run the E2E tests, you will first need to ensure you have installed Pytest and Selenium. You can find the suite of tests within todo_app/Selenium Tests/
Further details of the Pytest dependency can be found here: https://pypi.org/project/pytest/
Further details of the Selenium dependency can be found here: https://pypi.org/project/selenium/
As we are using Chrome for our Selenium test there is a dependency on the webdriver - chromedriver.exe This can be downloaded from https://sites.google.com/chromium.org/driver/ ensuring you are running the correct release to your browser. 

You can run the tests from the directory using poetry run pytest

docker run --env-file .env todo-app:test todo_app/Selenium_Tests/test_Selenium.py