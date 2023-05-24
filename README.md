# belvo_test
Tech test of DRF performed for Belvo company on position of Backend Engineer - Mid Level position

## Installation
### Installing with docker containers

> This option is the most indicated when the goal is to run in production mode.

Before you can execute the installing commands, please ensure these external requirements are already installed:
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/linux/)


To run the app on Docker containers, please execute the commands bellow:
```shell
# clone this repository
git clone git@github.com:samukasmk/belvo_test.git

# access new folder
cd belvo_test

# build and run the apps inside containers
docker-compose up --build -d
```

### Installing in your local machine
> This other option to run in your local machine (without Docker) is a very specific implementation for development purposes like debugging this app in your IDE.

> **If you want to run with Docker and you've installed with previous topic, please ignore these instructions bellow skipping to the next topic.**

To run this Django project in your local machine, execute the commands bellow:
```shell
# clone this repository
git clone https://github.com/samukasmk/belvo_test.git

# access new folder
cd belvo_test

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

## Using the REST API
Access the URL from your local:
[http://127.0.0.1/transactions/](http://127.0.0.1/transactions/)

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

## Running unit tests
```shell
pytest .
```

