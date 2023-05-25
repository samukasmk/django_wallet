import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from apps.wallet.models import FinancialTransaction


@pytest.fixture(scope="function")
def api_client():
    """ API Client to make REST API requests"""
    return APIClient()


def sample_transactions_data():
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
            {"reference": "000055",
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


def sample_outflow_transactions():
    """ Sample data of valid transactions

        always rebuilding the list of data to prevent problems of one test changing data from another """

    return [{"reference": "000151",
             "date": "2020-01-01",
             "amount": "-151.15",
             "type": "outflow",
             "category": "groceries",
             "user_email": "johndoe@email.com"}]


def sample_inflow_transactions():
    """ Sample data of valid transactions

        always rebuilding the list of data to prevent problems of one test changing data from another """

    return [{"reference": "000152",
             "date": "2020-01-11",
             "amount": "5500.93",
             "type": "inflow",
             "category": "salary",
             "user_email": "janedoe@email.com"}]


def normalize_dict_to_model(transaction_dict):
    """ Normalize dict object of a transaction to expected data in database """
    # normalizing type code
    if transaction_dict['type'] == 'inflow':
        transaction_dict['type'] = FinancialTransaction.TransactionType.inflow
    elif transaction_dict['type'] == 'outflow':
        transaction_dict['type'] = FinancialTransaction.TransactionType.outflow

    # normalizing amount
    transaction_dict['amount'] = float(transaction_dict['amount'])

    return transaction_dict


@pytest.fixture(scope="function")
def sample_transactions_models():
    return [baker.make('FinancialTransaction',
                       **normalize_dict_to_model(transaction_to_create))
            for transaction_to_create in sample_transactions_data()]
