from datetime import datetime
from decimal import Decimal

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


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


def sample_expected_payload_summary_by_user_email():
    """ Sample data of valid summary of total inflow and outflow for each user """

    return [{"user_email": "janedoe@email.com",
             "total_inflow": "2651.44",
             "total_outflow": "-761.85"},
            {"user_email": "johndoe@email.com",
             "total_inflow": "0.00",
             "total_outflow": "-51.13"}]


def sample_expected_payload_summary_by_category():
    """ Sample data REST API response of valid summary of each user transactions by inflow and outflow categories """

    return [['janedoe@email.com',
             {"inflow": {"salary": "2500.72",
                         "savings": "150.72"},
              "outflow": {"groceries": "-51.13",
                          "rent": "-560.00",
                          "transfer": "-150.72"}}],

            ['johndoe@email.com',
             {"inflow": {},
              "outflow": {"other": "-51.13"}}]]


def sample_expected_queryset_summary_by_category():
    """ Sample data of QuerySet result with summary of each user transactions by inflow and outflow categories """

    return [['janedoe@email.com',
             [{'type': 'inflow', 'category': 'salary', 'total': Decimal('2500.72')},
              {'type': 'inflow', 'category': 'savings', 'total': Decimal('150.72')},
              {'type': 'outflow', 'category': 'groceries', 'total': Decimal('-51.13')},
              {'type': 'outflow', 'category': 'rent', 'total': Decimal('-560.0')},
              {'type': 'outflow', 'category': 'transfer', 'total': Decimal('-150.72')}]],

            ['johndoe@email.com',
             [{'type': 'outflow', 'category': 'other', 'total': Decimal('-51.13')}]]]


def dict_to_model(transaction_dict):
    """ Normalize dict object of a transaction to expected data in database """
    # normalizing amount value
    transaction_dict.update(
        {'amount': Decimal(transaction_dict['amount']),
         'date': datetime.strptime(transaction_dict['date'], '%Y-%m-%d').date()})

    return transaction_dict


@pytest.fixture(scope="function")
def mock_db_transactions():
    return [baker.make('FinancialTransaction',
                       **dict_to_model(transaction_to_create))
            for transaction_to_create in sample_transactions_data()]
