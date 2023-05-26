import pytest
from typing import Sequence
from apps.wallet.models import FinancialTransaction
from apps.wallet.logic import summarize_all_transactions_by_user_email


@pytest.mark.django_db
def test_summarize_all_transactions_by_user_email(sample_transactions_models: Sequence[FinancialTransaction]) -> None:
    """ Test logic function of aggregation by user email """

    summarized_queryset = summarize_all_transactions_by_user_email()
    assert list(summarized_queryset) == [{'user_email': 'janedoe@email.com',
                                          'total_inflow': 2651.4399999999996,
                                          'total_outflow': -761.85},
                                         {'user_email': 'johndoe@email.com',
                                          'total_inflow': 0.0,
                                          'total_outflow': -51.13}]


@pytest.mark.django_db
def test_summarize_user_transactions_by_category(sample_transactions_models: Sequence[FinancialTransaction]) -> None:
    """ Test logic function to aggregate total inflow and outflow by categories for a specific user """

    summarized_queryset = summarize_user_transactions_by_category()
    assert list(summarized_queryset) == {"inflow": {"salary": 2500.72,
                                                    "savings": 150.72},
                                         "outflow": {"groceries": -51.13,
                                                     "rent": -560.00,
                                                     "transfer": -150.72}}
