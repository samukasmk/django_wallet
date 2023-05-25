import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    """ API Client to make REST API requests"""
    return APIClient()


def sample_transactions():
    """ Sample data of valid transactions

        always rebuilding the list of data to prevent problems of one test changing data from another """

    return [{"reference": "000051",
             "date": "2020-01-03",
             "amount": "-51.13",
             "type": "outflow",
             "category": "groceries",
             "user_email": "janedoe@email.com"},
            {"reference": "000052",
             "date": "2020-01-10",
             "amount": "2500.72",
             "type": "inflow",
             "category": "salary",
             "user_email": "janedoe@email.com"},
            {"reference": "000053",
             "date": "2020-01-10",
             "amount": "-150.72",
             "type": "outflow",
             "category": "transfer",
             "user_email": "janedoe@email.com"},
            {"reference": "000054",
             "date": "2020-01-13",
             "amount": "-560.00",
             "type": "outflow",
             "category": "rent",
             "user_email": "janedoe@email.com"},
            {"reference": "000051",
             "date": "2020-01-04",
             "amount": "-51.13",
             "type": "outflow",
             "category": "other",
             "user_email": "johndoe@email.com"},
            {"reference": "000689",
             "date": "2020-01-10",
             "amount": "150.72",
             "type": "inflow",
             "category": "savings",
             "user_email": "janedoe@email.com"}]
