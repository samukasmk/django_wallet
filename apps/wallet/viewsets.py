from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from apps.wallet.models import FinancialTransaction
from apps.wallet.serializers import (FinancialTransactionSerializer, SummaryAllTransactionsByUser,
                                     SummaryUserTransactionByCategory)
from apps.wallet.logic import summarize_all_transactions_by_user_email, summarize_user_transactions_by_category


class FinancialTransactionsViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        List all financial transactions
        or aggregate amount values if ?group_by=type is defined
        """
        # summarize amount by flow type if group_by query parameter is declared as type
        if request.GET.get('group_by') == 'type':
            return self.summary_all_transactions_by_user_email()

        # list all financial transactions by builtin methods
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create financial transactions for each object of bulk list
        """
        if isinstance(request.data, list):
            self.serializer_many = True
        return super().create(request, *args, **kwargs)

    def summary_all_transactions_by_user_email(self) -> Response:
        """
        Aggregate amount values of all transactions
        grouping by user
        """
        queryset = summarize_all_transactions_by_user_email()
        serializer = SummaryAllTransactionsByUser(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path=rf'(?P<user_email>{settings.EMAIL_REGEX})/summary')
    def summary_user_transactions_by_category(self, request: Request, user_email: str, *args, **kwargs) -> Response:
        """
        Aggregate amount values of user's transactions
        grouping by category
        """
        queryset = summarize_user_transactions_by_category(user_email)
        serializer = SummaryUserTransactionByCategory(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # overwriting builtin methods
    def __init__(self, *arg, **kwargs):
        """
        Overload ModelViewSet.__init__ method
        injecting new attribute self.serializer_many
        """
        super().__init__(*arg, **kwargs)
        self.serializer_many = None

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.

        Customization: add attribute serializer_many to manage many items.
        """
        if self.serializer_many is not None:
            kwargs['many'] = self.serializer_many
        return super().get_serializer(*args, **kwargs)
