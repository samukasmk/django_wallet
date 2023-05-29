import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_redirect_transaction_listing_to_transacations(api_client: APIClient) -> None:
    """
    Test listing redirections from: /transaction to: /transactions
    """

    # make api request
    response = api_client.get('/transaction')

    # check redirections
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == '/transactions'
