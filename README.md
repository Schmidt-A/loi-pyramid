# Legacy of Imphras
Originally started as a web application to serve information from an online game server on NWN for out of game activities.

Now moribund with possible ideas to have a primarily chat based web application game focused on roleplaying and storytelling.

## Installing

* Change directory into your newly created project.
```
cd loi_pyramid
```
* Create a Python virtual environment.
```
python3 -m venv env
```
* Switch into your environment.
```
source env/bin/activate
```
* Upgrade packaging tools.
```
pip3 install --upgrade pip setuptools
```
* Install the project in editable mode with its testing and linting requirements.
```
pip3 install -e ".[testing]"
pip3 install -e ".[linting]"
```
* Install setup.py requirements
```
python3 setup.py develop
```

## Local Data
### Set up the local database
```
initialize_loi_pyramid_db development.ini
```

Change the db script if you want to alter how the local data is stood up:
```/loi_pyramid/scripts/initializedb.py```

Fixtures are sourced from:
```loi_pyramid/tests/fixture_helper.py```

## Linting
Only run this from ```/loi_pyramid``` or subfolders otherwise it will go through the ```/env``` installs
```
pylint .
```

To automatically fix codestyle https://github.com/hhatto/autopep8
```
autopep8 --in-place --aggressive --aggressive -r -v .
```

## Testing 
### Unit Tests
```
pytest
```

To check coverage, add ```--cov=loi_pyramid```

## Running
Run your project.
```
pserve development.ini
```

The server will now be running at localhost port 6543:
```http://127.0.0.1:6543```