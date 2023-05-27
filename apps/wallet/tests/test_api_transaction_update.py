from typing import Sequence

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
        amount_transaction = float(transaction_to_get["amount"])

        # ensure current amount is equal of request value in mock
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["reference"]).amount == amount_transaction

        # increase or decrease new amount to change
        if amount_transaction > 0:
            amount_transaction = amount_transaction + 10000000.0
        elif amount_transaction < 0:
            amount_transaction = amount_transaction - 10000000.0

        # change amount and category
        transaction_to_get['amount'] = '{:.2f}'.format(amount_transaction)
        transaction_to_get['category'] = 'updated_category_by_put'

        # get existent object of database from api
        response = api_client.put(f'/transaction/{transaction_to_get["reference"]}', transaction_to_get)

        # check returned payload with updated data
        assert response.status_code == status.HTTP_200_OK
        assert response.data == transaction_to_get

        # check update on database
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["reference"]).amount == float(transaction_to_get["amount"])
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["reference"]).category == 'updated_category_by_put'
