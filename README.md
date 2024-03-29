# django_wallet
A straightforward REST API that stores financial transaction records made by each user, summarizing spending,
and receivables, and balances of transactions by category.

- **By:** Samuel Maciel Sampaio
- **Email:** <mailto:samuel.maciel.sampaio@gmail.com>
- **Github:** @samukasmk

## Installation

> This installation mode is the most indicated when the goal is to run in production mode.
> If you want to install without docker, directly in your machine please read the
> topic: [Extra: Working in your local machine (without docker)](#extra-working-in-your-local-machine-without-docker)

Before you can execute the installing commands, please ensure these external requirements are already installed:

- [Docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

To run this app on Docker containers, please execute the commands below:

```shell
# clone this repository
git clone git@github.com:samukasmk/django_wallet.git

# access new folder
cd django_wallet

# build and run the apps inside containers
docker-compose up --build -d
```

**Docker compose example:**

![.docs/gifs/docker-compose-up.gif](.docs/gifs/docker-compose-up.gif)

## Using the REST API

After `docker-compose` has created the new containers you can access them by URL and passing the content type
of: `application/json`

Example to access by `curl` tool:

```shell
curl -X GET http://127.0.0.1/transactions
```

### Using API by Swagger

Swagger is a great REST API documentation tool that works with OpenAPI 3 standards.

If you prefer I've configured Swagger in this project.

To access the API documentation you just need to click on the next URL [http://127.0.0.1](http://127.0.0.1)

> But don't forget to check if containers are created and running before accessing Swagger URL

**Swagger example:**

![.docs/images/home/swagger-1-home.png](.docs/images/home/swagger-1-home.png)

---

As requested in the test description, I created 4 endpoint variations of `/transactions` verb:

- create many transactions in bulk mode: `POST /transactions`
- list all existing transactions: `GET /transactions`
- summarize transactions by total inflows and outflows per user: `GET /transactions?group_by=type`
- summarize transactions grouped by category: `GET /transactions/{user_email}/summary`

I also created in addition, 4 more new endpoints variations of `/transaction` verb to:

- create a new single transaction record: `POST /transaction`
- retrieve a transaction record by reference id: `GET /transaction/{reference}`
- update all transaction fields information: `PUT /transaction/{reference}`
- update specific transaction fields information: `PATCH /transaction/{reference}`
- and deleting it: `DELETE /transaction/{reference}`

## Multiple transactions endpoints

### Create many transactions in bulk mode

```
POST /transactions
```

**Example:**

![.docs/images/many-transactions/swagger-2-create-many.png](.docs/images/many-transactions/swagger-2-create-many.png)

### List all existing transactions

```
GET /transactions
```

**Example:**

![.docs/images/many-transactions/swagger-3-list-all.png](.docs/images/many-transactions/swagger-3-list-all.png)

### Summarize transactions by total inflows and outflows per user

```
GET /transactions?group_by=type
```

**Example:**

![.docs/images/many-transactions/swagger-4-summary-by-user.png](.docs/images/many-transactions/swagger-4-summary-by-user.png)

### Summarize transactions grouped by category

```
GET /transactions/{user_email}/summary
```

**Example:**

![.docs/images/many-transactions/swagger-5-summary-by-category.png](.docs/images/many-transactions/swagger-5-summary-by-category.png)

## Specific transaction endpoints

### Create a new single transaction record

```
POST /transaction
```

**Example:**

![.docs/images/single-transaction/swagger-6-create-single.png](.docs/images/single-transaction/swagger-6-create-single.png)

### Retrieve a transaction record by reference id

```
GET /transaction/{reference}
```

**Example:**

![.docs/images/single-transaction/swagger-7-get-single.png](.docs/images/single-transaction/swagger-7-get-single.png)

### Update all transaction fields information

```
PUT /transaction/{reference}
```

**Example:**

![.docs/images/single-transaction/swagger-8-update-single.png](.docs/images/single-transaction/swagger-8-update-single.png)

### Update specific transaction fields information

```
PATCH /transaction/{reference}
```

**Example:**

![.docs/images/single-transaction/swagger-8-partial-update-single.png](.docs/images/single-transaction/swagger-8-partial-update-single.png)

### And deleting it

```
DELETE /transaction/{reference}
```

**Example:**

![.docs/images/single-transaction/swagger-9-delete.png](.docs/images/single-transaction/swagger-9-delete.png)

## Running unit tests (from docker container)

Since `docker-compose` has built with success the image containers
you can run the `unit tests` directly from `docker-compose` with the command:

```shell
docker-compose run --rm unit-tests
```

**Example:**

![.docs/gifs/docker-compose-unittests.gif](.docs/gifs/docker-compose-unittests.gif)

> Note: I covered as much as possible in terms of time, the variants of test scenarios,
> reaching the coverage level of 100%, but many tests can be improved in terms of
> performance, simplicity, and even cover unforeseen scenarios by coverage tool
> because I wrote them as quickly as possible in the time of I had

![.docs/images/tests/unit-tests-a-hundred-percent.png](.docs/images/tests/unit-tests-a-hundred-percent.png)

# Extra: Working in your local machine (without docker)

## Installing in your local machine

> This installation mode **(without Docker)** is a very specific implementation 
> for development purposes like debugging this app in your IDE.
> **If you want to run with Docker, please ignore the instructions below
> returning to the topic of [Installation](#installation).**
> To run this Django project on your local machine, execute the commands below:

To run this Django project in your local machine, execute the commands below:

```shell
# clone this repository
git clone https://github.com/samukasmk/django_wallet.git

# access new folder
cd django_wallet

# create new virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# install required libraries
pip install -r requirements.txt

# install, configure run your database by yourself (it can be alone in docker) like:
docker-compose up postgres

# set host address, db name, username, and password in the file: (settings.py)
# note: Even if you are just going to use Postgres on docker-compose alone and the Django app running
# in your machine, the current configuration is already working.
# Because I defined docker-compose.yml to expose the Postgres internal port for your localhost:5432
# --- 
# vim settings.py

# export the static files
./manage.py collectstatic

# create the database structure (for new databases installations)
./manage.py migrate

# run the webserver in DEBUG mode
DEBUG=TRUE ./manage.py runserver
```

## Running unit tests (without docker container)

```shell
# you can run unit tests from make commands:
make test

# or your run pytest directly from your IDE like
pytest .
```