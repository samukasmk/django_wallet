from django.conf import settings
from django.http import HttpResponseRedirect
from drf_spectacular.utils import extend_schema as swagger_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.wallet.models import FinancialTransaction
from apps.wallet.schemas import (create_many_transactions_schema,
                                 create_single_transaction_schema,
                                 list_many_transactions_schema,
                                 retrieve_single_transaction_schema,
                                 summary_user_transactions_by_category_schema,
                                 update_single_transaction_schema,
                                 partial_update_single_transaction_schema)
from apps.wallet.serializers import (FinancialTransactionSerializer,
                                     SummaryAllTransactionsByUser,
                                     SummaryUserTransactionByCategory)


class FinancialTransactionsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer

    @swagger_schema(**create_many_transactions_schema)
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create multiple financial transactions records in bulk operation.
        """
        self.serializer_many = True
        return super().create(request, *args, **kwargs)

    @swagger_schema(**list_many_transactions_schema)
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        1.) List all financial transactions records (without query params).

        2.) Return the summary with aggregated total_inflow and total_outflows per user (with param: ?group_by=type).
        """
        # summarize amount by flow type if group_by query parameter is declared as type
        if request.GET.get('group_by') == 'type':
            return self.summary_all_transactions_by_user_email()

        # list all financial transactions by builtin methods
        return super().list(request, *args, **kwargs)

    def summary_all_transactions_by_user_email(self) -> Response:
        """
        Aggregate amount values of all transactions grouping by user.
        """
        queryset = FinancialTransaction.objects.summarize_all_transactions_by_user_email()
        serializer = SummaryAllTransactionsByUser(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_schema(**summary_user_transactions_by_category_schema)
    @action(methods=['GET'], detail=False, url_path=rf'(?P<user_email>{settings.EMAIL_REGEX})/summary')
    def summary_user_transactions_by_category(self, request: Request, user_email: str, *args, **kwargs) -> Response:
        """
        Return user's transactions summary, grouping the sum transactions amount by categories.
        """
        queryset = FinancialTransaction.objects.summarize_user_transactions_by_category(user_email)
        serializer = SummaryUserTransactionByCategory(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # overwriting builtin methods
    def __init__(self, *arg, **kwargs):
        """
        Overload ModelViewSet.__init__ method injecting new attribute self.serializer_many
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


class FinancialTransactionViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer
    lookup_field = 'reference'

    # http_method_names = ['get', 'post', 'put', 'delete', 'head']

    @swagger_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        """
        Redirect listing from: /transaction to: /transactions.
        """
        return HttpResponseRedirect(redirect_to='/transactions')

    @swagger_schema(**create_single_transaction_schema)
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create single financial transaction records.
        """
        return super().create(request, *args, **kwargs)

    @swagger_schema(**retrieve_single_transaction_schema)
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Get single financial transaction records by reference id.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_schema(**update_single_transaction_schema)
    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Update full fields a single financial transaction record by reference id.

        Note: the reference field is read-only in payload, and it can't be changed by put.
        """
        return super().update(request, *args, **kwargs)

    @swagger_schema(**partial_update_single_transaction_schema)
    def partial_update(self, request, *args, **kwargs):
        """
        Update specific fields of a single financial transaction record by reference id.

        Note: the reference field is read-only in payload, and it can't be changed by patch.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Delete single financial transaction records by reference id.
        """
        return super().destroy(request, *args, **kwargs)
