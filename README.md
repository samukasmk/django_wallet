# belvo_wallet
A very simple REST API that stores financial transactions made by each user, summarizes spending and receivables and accounts transaction balances by category. 

This project is part of the techincal test performed for Belvo company on position of Backend Engineer - Mid Level position.

## Installation
> This installation mode is the most indicated when the goal is to run in production mode.
> If you want to install without docker, directly in your machine please read the topic: [Extra: Working in your local machine (without docker)](#extra-working-in-your-local-machine-without-docker)

Before you can execute the installing commands, please ensure these external requirements are already installed:
- [Docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)


To run this app on Docker containers, please execute the commands bellow:
```shell
# clone this repository
git clone git@github.com:samukasmk/belvo_wallet.git

# access new folder
cd belvo_wallet

# build and run the apps inside containers
docker-compose up --build -d
```

**Example:**

![.docs/gifs/docker-compose-up.gif](.docs/gifs/docker-compose-up.gif) 

## Using the REST API
After `docker-compose` has created the new containers you can access directly by URL: [http://127.0.0.1/transactions/](http://127.0.0.1/transactions/)

from your preferred http client like `chrome browser`, `postman`, `curl`, `python requests` or others.

### Get users' transactions
```
GET /transactions
```

```
[
    {
        "reference": "000051",
        "date": "2020-01-03",
        "amount": "-51.13",
        "type": "outflow",
        "category": "groceries",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000052",
        "date": "2020-01-10",
        "amount": "2500.72",
        "type": "inflow",
        "category": "salary",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000053",
        "date": "2020-01-10",
        "amount": "-150.72",
        "type": "outflow",
        "category": "transfer",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000054",
        "date": "2020-01-13",
        "amount": "-560.00",
        "type": "outflow",
        "category": "rent",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000051",
        "date": "2020-01-04",
        "amount": "-51.13",
        "type": "outflow",
        "category": "other",
        "user_email": "johndoe@email.com"
    },
    {
        "reference": "000689",
        "date": "2020-01-10",
        "amount": "150.72",
        "type": "inflow",
        "category": "savings" ,
        "user_email": "janedoe@email.com"
    }
]
```

### Get transactions summary by user
```
GET /transactions?group_by=type
```

```
[
    {
        "user_email": "janedoe@email.com",
        "total_inflow": "2651.44",
        "total_outflow": "-761.85"
    },
    {
        "user_email": "johndoe@email.com",
        "total_inflow": "0.00",
        "total_outflow": "-51.13"
    }
]
```

### Get transactions summary by category
```
GET /transactions/{user_email}/summary
```

```
{
    "inflow": {
        "salary": "2500.72",
        "savings": "150.72"
    },
    "outflow": {
        "groceries": "-51.13",
        "rent": "-560.00",
        "transfer": "-150.72"
    }
}
```

## Running unit tests (from docker container)
Since docker-compose has built with success your image containers
you can run the `unit tests` directly from `docker-compose` with command: 

```shell
docker-compose run --rm unittests
```

**Example:**

![.docs/gifs/docker-compose-unittests.gif](.docs/gifs/docker-compose-unittests.gif)


# Extra: Working in your local machine (without docker)  

## Installing in your local machine
> This installation mode is a very specific implementation to install **(without Docker)** for development purposes like debugging this app in your IDE.
> **If you want to run with Docker, please ignore these instructions bellow returning to topic [Installation](#installation).**

To run this Django project in your local machine, execute the commands bellow:
```shell
# clone this repository
git clone https://github.com/samukasmk/belvo_wallet.git

# access new folder
cd belvo_wallet

# create new virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# install required libraries
pip install -r requirements.txt

# export the static files
./manage.py collectstatic

# create the database structure
./manage.py migrate

# run the webserver
./manage.py runserver
```

## Running unit tests (without docker container)
```shell
make test

# or your run pytest directly from your IDE like
pytest .
```