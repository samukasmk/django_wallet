from typing import Sequence

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_list_transactions(api_client: APIClient,
                           mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """
    Test endpoint to get all transactions
    """
    transactions_to_get = sample_transactions_data()

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(transactions_to_get)

    # get existent objects of database from api
    response = api_client.get('/transactions')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == transactions_to_get
