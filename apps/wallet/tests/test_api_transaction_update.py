from decimal import Decimal
from typing import Sequence
from random import shuffle

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_update_transactions_by_put(api_client: APIClient,
                                    mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """ Test endpoint to update all informations in a transaction """
    transactions_to_get = sample_transactions_data()

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(transactions_to_get)

    # get each transaction on database one by one
    for transaction_to_get in transactions_to_get:
        amount_transaction = Decimal(transaction_to_get['amount'])

        # ensure current amount is equal of request value in mock
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get['reference']).amount == amount_transaction

        # increase or decrease new amount to change
        if amount_transaction > 0:
            amount_transaction = amount_transaction + Decimal('10000000.00')
        elif amount_transaction < 0:
            amount_transaction = amount_transaction - Decimal('10000000.00')

        # change amount and category in json payload
        transaction_to_get['amount'] = str(amount_transaction)
        transaction_to_get['category'] = 'updated_category_by_put'

        # get existent object of database from api
        response = api_client.put(f'/transaction/{transaction_to_get["reference"]}', transaction_to_get)

        # check returned payload with updated data
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == transaction_to_get

        # check update on database
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get['reference']).amount == Decimal(transaction_to_get['amount'])
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get['reference']).category == 'updated_category_by_put'


@pytest.mark.django_db
def test_update_transactions_by_patch(api_client: APIClient,
                                      mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    # get a json payload randomly shuffled
    all_json_transactions = sample_transactions_data()
    shuffle(all_json_transactions)
    transaction_to_patch = all_json_transactions[0]

    # check model existence in db
    assert FinancialTransaction.objects.get(
        reference=transaction_to_patch["reference"]).user_email == transaction_to_patch['user_email']

    # make patch request
    new_email_address = 'updated_email@email.com'
    response = api_client.patch(f'/transaction/{transaction_to_patch["reference"]}',
                                {'user_email': new_email_address})

    # check http status
    assert response.status_code == status.HTTP_200_OK

    # check specific value is updated
    transaction_to_patch['user_email'] = new_email_address
    assert response.json() == transaction_to_patch
