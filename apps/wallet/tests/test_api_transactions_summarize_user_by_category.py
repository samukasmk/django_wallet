from typing import Sequence

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import (
    sample_expected_payload_summary_by_category, sample_transactions_data)


@pytest.mark.django_db
@pytest.mark.parametrize('user_email, user_summary_by_category', sample_expected_payload_summary_by_category())
def test_summarize_all_transactions_by_user(api_client: APIClient,
                                            mock_db_transactions: Sequence[FinancialTransaction],
                                            user_email: str,
                                            user_summary_by_category: dict) -> None:
    """
    Test endpoint to summarize users' transactions by category
    """
    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(sample_transactions_data())

    # get existent objects of database from api
    response = api_client.get(f'/transactions/{user_email}/summary')
    assert response.status_code == status.HTTP_200_OK

    # assert response
    assert response.json() == user_summary_by_category
