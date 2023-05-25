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


def sample_summary_all_transactions_by_user_email():
    """ Sample data of valid summary of total inflow and outflow for each user """

    return [{"user_email": "janedoe@email.com",
             "total_inflow": "2651.44",
             "total_outflow": "-761.85"},
            {"user_email": "johndoe@email.com",
             "total_inflow": "0.00",
             "total_outflow": "-51.13"}]


def sample_summary_user_transactions_by_category():
    """ Sample data of valid summary of each user transactions by inflow and outflow categories """

    return [['janedoe@email.com',
             {"inflow": {"salary": "2500.72",
                         "savings": "150.72"},
              "outflow": {"groceries": "-51.13",
                          "rent": "-560.00",
                          "transfer": "-150.72"}}],
            ['johndoe@email.com',
             {"inflow": {},
              "outflow": {"other": "-51.13"}}]]


def normalize_dict_to_model(transaction_dict):
    """ Normalize dict object of a transaction to expected data in database """
    # normalizing type code
    if transaction_dict['type'] == 'inflow':
        transaction_dict['type'] = FinancialTransaction.TransactionType.inflow
    elif transaction_dict['type'] == 'outflow':
        transaction_dict['type'] = FinancialTransaction.TransactionType.outflow

    # normalizing amount value
    transaction_dict['amount'] = float(transaction_dict['amount'])

    return transaction_dict


@pytest.fixture(scope="function")
def sample_transactions_models():
    return [baker.make('FinancialTransaction',
                       **normalize_dict_to_model(transaction_to_create))
            for transaction_to_create in sample_transactions_data()]
