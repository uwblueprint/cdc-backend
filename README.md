## Getting Started (Contributors Only)

1. Clone this repo and the frontend repo (cdc-frontend)
2. Grab the secrets
3. todo: continued steps to get project set up locally

---

## About Calgary Distress Center

todo

### Team

Project Lead: [Ahmed Hamodi](https://github.com/ahmedhamodi)\
Product Manager: [Aaron Abraham](https://github.com/aaronabraham311)\
Designers: [Jack Zhang](https://github.com/fakesquid), [Kouthar Waled](https://github.com/kouthar)\
Developers: [Jay Dhulia](https://github.com/jaydhulia), [Dhruvin Balar](https://github.com/drbalar), [Vivian Liu](https://github.com/vivianliu0), [Kevin Hu](https://github.com/andstun)

---

## Local Development Setup

### Frontend

See cdc-frontend for frontend setup.

### Backend

#### Python setup
1. Ensure that you have Python 3.9.1 on your system by running `python3 --version`. If you don't, please upgrade your Python.
1. If you don't have an environment setup already within the repo: `python3 -m venv env`
    Note: you will only need to do the above command once.
1. Activate the virtual environment: `. ./env/bin/activate`
1. Install the requirements: `pip install -r requirements.txt`

Once you have the requirements installed, you should be able to develop by just activating the environment (step 2).

#### Python - adding a new requirement
1. Update the file `requirements.in` with the name of the library that you want to add.
1. Install pip-compile if you don't have it already - `pip install pip-tools`.
1. Run `pip-compile requirements.in`
1. Download the updated packages `pip install -r requirements.txt`
1. Check locally to ensure that you haven't broken anything ;) 

To run the backend server:

```
todo
```

To call any APIs that require authentication without the frontend running (ex. using curl or Postman), you'll need an access token. You can generate a token for your account this with the command:

```
todo
```

This script will output a JSON object – you can use the `idToken` value and provide it as a bearer token to your API calls. This token expires every hour, and you can rerun this script to generate a new one.

## Deployment

todo
