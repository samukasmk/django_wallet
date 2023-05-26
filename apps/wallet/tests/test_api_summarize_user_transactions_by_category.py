import pytest
from typing import Sequence
from rest_framework import status
from rest_framework.test import APIClient
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data, sample_summary_user_transactions_by_category


@pytest.mark.django_db
@pytest.mark.parametrize('user_email, user_summary_by_category', sample_summary_user_transactions_by_category())
def test_summarize_all_transactions_by_user(api_client: APIClient,
                                            sample_transactions_models: Sequence[FinancialTransaction],
                                            user_email: str,
                                            user_summary_by_category: dict) -> None:
    """ Test endpoint to summarize users' transactions by category """
    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(sample_transactions_data())

    # get existent objects of database from api
    response = api_client.get(f'/transactions/{user_email}/summary')
    assert response.status_code == status.HTTP_200_OK

    # assert response
    assert response.data == user_summary_by_category
