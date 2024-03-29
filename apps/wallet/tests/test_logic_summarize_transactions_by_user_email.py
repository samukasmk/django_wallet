from decimal import Decimal
from typing import List, Sequence

import pytest

from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import \
    sample_expected_queryset_summary_by_category


@pytest.mark.django_db
def test_summarize_all_transactions_by_user_email(mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """
    Test logic function of aggregation by user email
    """
    summarized_queryset = FinancialTransaction.objects.summarize_all_transactions_by_user_email()
    assert list(summarized_queryset) == [{'user_email': 'janedoe@email.com',
                                          'total_inflow': Decimal('2651.44'),
                                          'total_outflow': Decimal('-761.85')},
                                         {'user_email': 'johndoe@email.com',
                                          'total_inflow': Decimal('0.00'),
                                          'total_outflow': Decimal('-51.13')}]


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
    summarized_queryset = FinancialTransaction.objects.summarize_user_transactions_by_category(user_email)
    assert list(summarized_queryset) == expected_queryset_result
