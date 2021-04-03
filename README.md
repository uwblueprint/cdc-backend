# Getting Started (Contributors Only)

1. Clone this repo and the frontend repo (cdc-frontend)
2. Grab the secrets
3. todo: continued steps to get project set up locally

---

# About Calgary Distress Center

todo

# Team

Project Lead: [Ahmed Hamodi](https://github.com/ahmedhamodi)\
Product Manager: [Aaron Abraham](https://github.com/aaronabraham311)\
Designers: [Jack Zhang](https://github.com/fakesquid), [Kouthar Waled](https://github.com/kouthar)\
Developers: [Jay Dhulia](https://github.com/jaydhulia), [Dhruvin Balar](https://github.com/drbalar), [Amolik Singh](https://github.com/amoliksingh), [Vivian Liu](https://github.com/vivianliu0), [Kevin Hu](https://github.com/andstun)

---

# Local Development Setup

## Frontend

See cdc-frontend for frontend setup.

## Backend

### Python setup

1. Ensure that you have Python 3.9.1 on your system by running `python3 --version`. If you don't, please upgrade your Python.
1. If you don't have an environment setup already within the repo: `python3 -m venv env`
   - Note: you will only need to do the above command once.
1. Activate the virtual environment.
   - On a mac operating system, use: `. ./env/bin/activate`
   - On a windows operating system, use: `source ./env/Scripts/activate`
1. Install `Postgres` - Version 12. Choose user "Postgres" with blank password for local development.
   - On Mac, the recommended tool for managing your Postgres installation is [Postgres App](https://postgresapp.com/)
   - On Windows, download Postgres from [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) and then use the script in `scripts/PSQL Server Management.bat` to start/stop your Postgres Server
1. Once Postgres is installed, create a database with the name: `postgres_cdc_dev`
1. Install the requirements, and setup Postgres: `make install`

Note: Every time you run `git commit` in this repo, it will run some lint checks. It won't let you commit unless the lint checks pass. Note that this means you may have to run `git commit` multiple times, as each `git commit` will attempt to fix the files! Some files may fail to auto-fix, in which case, you will have to ensure you fix them.

Once you have the requirements installed, you should be able to develop by just activating the environment (step 2).

### Python - adding a new requirement

1. Update the file `requirements.in` with the name of the library that you want to add.
1. Install pip-compile if you don't have it already - `pip install pip-tools`.
1. Run `pip-compile requirements.in`
1. Download the updated packages `pip install -r requirements.txt`
1. Check locally to ensure that you haven't broken anything

### Running the backend repo

#### PyCharm

1. The run configurations should automatically be loaded and working, select the `dev` environment and hit the play button. Contact Jay if you have trouble setting this up.

#### Mac

1. Ensure you are in the root directory, and your virtual env is activated. Also make sure your Postgres is running.
1. If you have not done so recently, run `make install` as it will update any schema changes.
1. Run `export PYTHONPATH=.`
1. Run `export CONFIG_PATH=configs/dev-config.yaml`
1. Run `python app/__main__.py`
1. You should see a `SERVER STARTED` message along with configuration details

#### Windows

1. Ensure you are in the root directory, and your virtual env is activated. Also make sure your Postgres is running.
1. Run `set PYTHONPATH=.`
1. Run `set CONFIG_PATH=configs/dev-config.yaml`
1. If you have not done so recently, run the scripts to create and populate the database:
   ```
      python scripts/create-tables.py
      python scripts/insert_data.py
   ```
1. Run `python app/__main__.py`
1. You should see a `SERVER STARTED` message along with configuration details

To call any APIs that require authentication without the frontend running (ex. using curl or Postman), you'll need an access token. You can generate a token for your account this with the command:

```
todo
```

This script will output a JSON object – you can use the `idToken` value and provide it as a bearer token to your API calls. This token expires every hour, and you can rerun this script to generate a new one.

## Deployment

todo
