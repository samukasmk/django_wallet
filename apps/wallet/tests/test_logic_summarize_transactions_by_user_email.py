from typing import List, Sequence

import pytest

from apps.wallet.logic import (summarize_all_transactions_by_user_email,
                               summarize_user_transactions_by_category)
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import \
    sample_expected_queryset_summary_by_category


@pytest.mark.django_db
def test_summarize_all_transactions_by_user_email(mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """
    Test logic function of aggregation by user email
    """
    summarized_queryset = summarize_all_transactions_by_user_email()
    assert list(summarized_queryset) == [{'user_email': 'janedoe@email.com',
                                          'total_inflow': 2651.4399999999996,
                                          'total_outflow': -761.85},
                                         {'user_email': 'johndoe@email.com',
                                          'total_inflow': 0.0,
                                          'total_outflow': -51.13}]


@pytest.mark.django_db
@pytest.mark.parametrize("user_email, expected_queryset_result",
                         sample_expected_queryset_summary_by_category())
def test_summarize_user_transactions_by_category(
        user_email: str,
        expected_queryset_result: List[dict],
        mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """
    Test logic function of aggregation by category
    """
    summarized_queryset = summarize_user_transactions_by_category(user_email)
    assert list(summarized_queryset) == expected_queryset_result
