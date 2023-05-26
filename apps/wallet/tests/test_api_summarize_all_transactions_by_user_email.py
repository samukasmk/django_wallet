import pytest
from typing import Sequence
from rest_framework import status
from rest_framework.test import APIClient
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data, sample_summary_all_transactions_by_user_email


@pytest.mark.django_db
def test_summarize_all_transactions_by_user(api_client: APIClient,
                                            sample_transactions_models: Sequence[FinancialTransaction]) -> None:
    """ Test endpoint to summarize all transactions by user """
    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(sample_transactions_data())

    # get existent objects of database from api
    response = api_client.get('/transactions/?group_by=type')
    assert response.status_code == status.HTTP_200_OK

    # assert response
    assert response.data == sample_summary_all_transactions_by_user_email()
